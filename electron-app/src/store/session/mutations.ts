import { MutationTree } from 'vuex';
import { Currency } from '@/model/currency';
import { defaultState, SessionState } from '@/store/session/state';
import {
  AccountingSettings,
  AccountingSettingsUpdate,
  GeneralSettings,
  Tags
} from '@/typing/types';

export const mutations: MutationTree<SessionState> = {
  defaultCurrency(state: SessionState, currency: Currency) {
    state.settings = Object.assign(state.settings, {
      selectedCurrency: currency
    });
  },
  login(
    state: SessionState,
    payload: { username: string; newAccount: boolean }
  ) {
    const { username, newAccount } = payload;
    state.logged = true;
    state.newAccount = newAccount;
    state.username = username;
  },
  settings(state: SessionState, settings: GeneralSettings) {
    state.settings = Object.assign(state.settings, settings);
  },
  privacyMode(state: SessionState, privacyMode: boolean) {
    state.privacyMode = privacyMode;
  },
  scrambleData(state: SessionState, scrambleData: boolean) {
    state.scrambleData = scrambleData;
  },
  premium(state: SessionState, premium: boolean) {
    state.premium = premium;
  },
  premiumSync(state: SessionState, premiumSync: boolean) {
    state.premiumSync = premiumSync;
  },
  accountingSettings(
    state: SessionState,
    accountingSettings: AccountingSettings
  ) {
    state.accountingSettings = { ...accountingSettings };
  },
  updateAccountingSetting(
    state: SessionState,
    setting: AccountingSettingsUpdate
  ) {
    state.accountingSettings = { ...state.accountingSettings, ...setting };
  },
  nodeConnection(state: SessionState, nodeConnection: boolean) {
    state.nodeConnection = nodeConnection;
  },
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  reset(state: SessionState) {
    state = Object.assign(state, defaultState());
  },
  syncConflict(state: SessionState, syncConflict: string) {
    state.syncConflict = syncConflict;
  },
  tags(state: SessionState, tags: Tags) {
    state.tags = { ...tags };
  }
};
