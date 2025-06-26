import { Client } from '../domains/client';

export class ClientFormState {
  readonly clientId: string;
  readonly branding: string;
  readonly client: Client | null;
  readonly error: string;

  constructor(
    clientId: string = '',
    branding: string = '',
    client: Client | null = null,
    error: string = ''
  ) {
    this.clientId = clientId;
    this.branding = branding;
    this.client = client;
    this.error = error;
  }

  isValid(): boolean {
    return this.clientId.trim() !== '' && this.branding.trim() !== '';
  }
}

export class ClientFormActions {
  updateClientId(state: ClientFormState, clientId: string): ClientFormState {
    return new ClientFormState(
      clientId,
      state.branding,
      state.client,
      ''
    );
  }

  updateBranding(state: ClientFormState, branding: string): ClientFormState {
    return new ClientFormState(
      state.clientId,
      branding,
      state.client,
      ''
    );
  }

  createClient(state: ClientFormState): ClientFormState {
    try {
      if (!state.clientId.trim()) {
        return new ClientFormState(
          state.clientId,
          state.branding,
          null,
          'Client ID cannot be empty'
        );
      }

      const client = new Client({
        id: state.clientId,
        branding: {
          name: state.branding,
          logo: '',
          primaryColor: '#000000'
        }
      });
      return new ClientFormState(
        state.clientId,
        state.branding,
        client,
        ''
      );
    } catch (error) {
      return new ClientFormState(
        state.clientId,
        state.branding,
        null,
        error instanceof Error ? error.message : 'Unknown error'
      );
    }
  }
}