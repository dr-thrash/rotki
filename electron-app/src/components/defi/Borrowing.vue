<template>
  <progress-screen v-if="loading">
    <template #message>
      Please wait while your vaults are getting loaded...
    </template>
  </progress-screen>
  <v-container v-else>
    <v-row>
      <v-col cols="12">
        <h2>MakerDAO Vaults</h2>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <stat-card title="Total collateral locked">
          <amount-display
            :value="makerDAOVaultSummary.totalCollateralUsd"
            show-currency="symbol"
            fiat-currency="USD"
          ></amount-display>
        </stat-card>
      </v-col>
      <v-col>
        <stat-card title="Total debt">
          <amount-display
            :value="makerDAOVaultSummary.totalDebt"
            asset="DAI"
          ></amount-display>
        </stat-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-autocomplete
          v-model="selection"
          class="borrowing__vault-selection"
          label="Vault"
          item-key="identifier"
          :items="makerDAOVaults"
          item-text="identifier"
        ></v-autocomplete>
      </v-col>
    </v-row>
    <vault :vault="selectedVault" />
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { createNamespacedHelpers } from 'vuex';
import Vault from '@/components/defi/Vault.vue';
import AmountDisplay from '@/components/display/AmountDisplay.vue';
import StatCard from '@/components/display/StatCard.vue';
import ProgressScreen from '@/components/helper/ProgressScreen.vue';
import { MakerDAOVault } from '@/services/types-model';
import {
  MakerDAOVaultModel,
  MakerDAOVaultSummary
} from '@/store/balances/types';

const { mapGetters } = createNamespacedHelpers('balances');

@Component({
  computed: {
    ...mapGetters(['makerDAOVaults', 'makerDAOVaultSummary'])
  },
  components: { AmountDisplay, StatCard, Vault, ProgressScreen }
})
export default class Borrowing extends Vue {
  loading: boolean = false;
  selection: number = -1;
  makerDAOVaults!: MakerDAOVaultModel[];
  makerDAOVaultSummary!: MakerDAOVaultSummary;

  get selectedVault(): MakerDAOVault | MakerDAOVaultModel | null {
    return (
      this.makerDAOVaults.find(vault => vault.identifier === this.selection) ??
      null
    );
  }

  async mounted() {
    this.loading = true;
    await this.$store.dispatch('balances/fetchMakerDAOVaults');
    this.loading = false;
    await this.$store.dispatch('balances/fetchMakerDAOVaultDetails');
  }
}
</script>

<style scoped></style>
