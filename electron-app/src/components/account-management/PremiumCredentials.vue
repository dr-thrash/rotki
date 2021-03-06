<template>
  <div>
    <v-row no-gutters>
      <v-checkbox
        :value="enabled"
        label="Enable Premium"
        off-icon="fa fa-square-o"
        @change="enabledChanged"
      ></v-checkbox>
      <v-tooltip bottom>
        <template #activator="{ on }">
          <v-icon small class="mb-3 ml-1" v-on="on">fa fa-info-circle</v-icon>
        </template>
        <div>
          Enabling premium for a new account will restore the database
          associated with these credentials from the server. <br />
          Ensure that the account uses the same password as the database
          originally backed up.
        </div>
      </v-tooltip>
    </v-row>
    <div v-if="enabled">
      <v-text-field
        :value="apiKey"
        :disabled="loading"
        class="premium-settings__fields__api-key"
        :append-icon="showKey ? 'fa-eye' : 'fa-eye-slash'"
        prepend-icon="fa-key"
        :type="showKey ? 'text' : 'password'"
        :rules="apiKeyRules"
        label="Rotkehlchen API Key"
        @input="apiKeyChanged"
        @click:append="showKey = !showKey"
      ></v-text-field>
      <v-text-field
        :value="apiSecret"
        :disabled="loading"
        class="premium-settings__fields__api-secret"
        :append-icon="showSecret ? 'fa-eye' : 'fa-eye-slash'"
        prepend-icon="fa-user-secret"
        :type="showSecret ? 'text' : 'password'"
        label="Rotkehlchen API Secret"
        :rules="apiSecretRules"
        @input="apiSecretChanged"
        @click:append="showSecret = !showSecret"
      ></v-text-field>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Emit, Prop, Vue, Watch } from 'vue-property-decorator';

@Component({})
export default class PremiumCredentials extends Vue {
  @Prop({ required: true })
  loading!: boolean;
  @Prop({ required: true })
  enabled!: boolean;
  @Prop({ required: true })
  apiSecret!: string;
  @Prop({ required: true })
  apiKey!: string;

  showKey: boolean = false;
  showSecret: boolean = false;

  @Watch('enabled')
  onEnabledChange() {
    if (!this.enabled) {
      this.apiKeyChanged('');
      this.apiSecretChanged('');
    }
  }

  readonly apiKeyRules = [(v: string) => !!v || 'The API key cannot be empty'];
  readonly apiSecretRules = [
    (v: string) => !!v || 'The API secret cannot be empty'
  ];

  @Emit()
  apiKeyChanged(_apiKey: string) {}

  @Emit()
  apiSecretChanged(_apiSecret: string) {}

  @Emit()
  enabledChanged(_enabled: boolean) {}
}
</script>

<style scoped lang="scss"></style>
