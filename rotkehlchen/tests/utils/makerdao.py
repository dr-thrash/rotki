import types
from typing import Dict, List, NamedTuple, Tuple
from unittest.mock import patch

from web3 import Web3

from rotkehlchen.chain.ethereum.makerdao import RAY, WAD, MakerDAOVault
from rotkehlchen.constants.ethereum import (
    MAKERDAO_GET_CDPS,
    MAKERDAO_PROXY_REGISTRY,
    MAKERDAO_SPOT,
    MAKERDAO_VAT,
)
from rotkehlchen.fval import FVal
from rotkehlchen.tests.utils.factories import ZERO_ETH_ADDRESS
from rotkehlchen.typing import ChecksumEthAddress


class VaultTestData(NamedTuple):
    vaults: List[MakerDAOVault]
    proxy_mappings: Dict[ChecksumEthAddress, ChecksumEthAddress]
    mock_contracts: List[str]


class MockCaller:
    def __init__(self, test_data: VaultTestData, **kwargs) -> None:
        self.test_data = test_data
        for attr, value in kwargs.items():
            # Set the callable given from kwarg as a bound class method
            setattr(self, attr, types.MethodType(value, self))


class MockContract:
    def __init__(self, test_data, **kwargs):
        self.caller = MockCaller(test_data, **kwargs)


def mock_get_cdps_asc(
        self,
        cdp_manager_address,  # pylint: disable=unused-argument
        proxy,  # pylint: disable=unused-argument
) -> List[List]:
    result: List[List] = [[], [], []]
    for entry in self.test_data.vaults:
        result[0].append(entry.identifier)
        result[1].append(entry.urn)
        ilk = bytearray(entry.name.encode())
        ilk.extend(
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
        )
        result[2].append(ilk)

    return result


def mock_registry_proxies(self, address) -> ChecksumEthAddress:
    return self.test_data.proxy_mappings.get(address, ZERO_ETH_ADDRESS)


def mock_vat_urns(
        self,
        ilk,  # pylint: disable=unused-argument
        urn,
) -> Tuple[FVal, FVal]:
    for vault in self.test_data.vaults:
        if vault.urn == urn:
            result_a = vault.collateral_amount * WAD
            rate = 100
            result_b = ((vault.debt_value * RAY) / rate) * WAD
            return result_a, result_b

    raise AssertionError(f'Could not find a mock for vat urns for urn {urn}')


def mock_vat_ilks(self, ilk) -> Tuple[int, int, FVal]:
    for vault in self.test_data.vaults:
        vault_ilk = bytearray(vault.name.encode())
        vault_ilk.extend(
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
        )
        if vault_ilk == ilk:
            rate = 100
            price = vault.collateral_usd_value / vault.collateral_amount
            spot = (price / vault.liquidation_ratio) * RAY
            whatever = 1
            return whatever, rate, spot

    raise AssertionError(f'Could not find a mock for vat ilks for ilk {ilk}')


def mock_spot_ilks(self, ilk) -> Tuple[int, FVal]:
    for vault in self.test_data.vaults:
        vault_ilk = bytearray(vault.name.encode())
        vault_ilk.extend(
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
        )
        if vault_ilk == ilk:
            whatever = 1
            mat = vault.liquidation_ratio * RAY
            return whatever, mat

    raise AssertionError(f'Could not find a mock for spot ilks for ilk {ilk}')


def create_web3_mock(web3: Web3, test_data: VaultTestData):
    def mock_contract(address, abi):  # pylint: disable=unused-argument
        mock_proxy_registry = (
            address == MAKERDAO_PROXY_REGISTRY.address and
            'ProxyRegistry' in test_data.mock_contracts
        )
        if address == MAKERDAO_GET_CDPS.address and 'GetCDPS' in test_data.mock_contracts:
            return MockContract(test_data, getCdpsAsc=mock_get_cdps_asc)
        elif mock_proxy_registry:
            return MockContract(test_data, proxies=mock_registry_proxies)
        elif address == MAKERDAO_VAT.address and 'VAT' in test_data.mock_contracts:
            return MockContract(test_data, urns=mock_vat_urns, ilks=mock_vat_ilks)
        elif address == MAKERDAO_SPOT.address and 'SPOT' in test_data.mock_contracts:
            return MockContract(test_data, ilks=mock_spot_ilks)
        else:
            raise AssertionError('Got unexpected address for contract during tests')

    return patch.object(
        web3.eth,
        'contract',
        side_effect=mock_contract,
    )
