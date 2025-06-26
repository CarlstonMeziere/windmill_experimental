import { ClientFormState, ClientFormActions } from '../../src/ui/clientForm';
import { Client } from '../../src/domains/client';

describe('ClientForm UI Logic', () => {
  it('should initialize with empty form state', () => {
    const formState = new ClientFormState();
    
    expect(formState.clientId).toBe('');
    expect(formState.branding).toBe('');
    expect(formState.client).toBeNull();
    expect(formState.error).toBe('');
    expect(formState.isValid()).toBe(false);
  });

  it('should update client id', () => {
    const formState = new ClientFormState();
    const actions = new ClientFormActions();
    
    const newState = actions.updateClientId(formState, 'test-client-123');
    
    expect(newState.clientId).toBe('test-client-123');
    expect(newState.branding).toBe('');
    expect(newState.error).toBe('');
  });

  it('should update branding', () => {
    const formState = new ClientFormState();
    const actions = new ClientFormActions();
    
    const newState = actions.updateBranding(formState, 'Acme Corp');
    
    expect(newState.branding).toBe('Acme Corp');
    expect(newState.clientId).toBe('');
    expect(newState.error).toBe('');
  });

  it('should validate form when both fields filled', () => {
    const formState = new ClientFormState('test-123', 'Acme');
    
    expect(formState.isValid()).toBe(true);
  });

  it('should not validate form when client id empty', () => {
    const formState = new ClientFormState('', 'Acme');
    
    expect(formState.isValid()).toBe(false);
  });

  it('should not validate form when branding empty', () => {
    const formState = new ClientFormState('test-123', '');
    
    expect(formState.isValid()).toBe(false);
  });

  it('should create client successfully', () => {
    const formState = new ClientFormState('test-123', 'Acme Corp');
    const actions = new ClientFormActions();
    
    const newState = actions.createClient(formState);
    
    expect(newState.client).not.toBeNull();
    expect(newState.client!.id).toBe('test-123');
    expect(newState.client!.branding.name).toBe('Acme Corp');
    expect(newState.error).toBe('');
  });

  it('should handle client creation error', () => {
    const formState = new ClientFormState('', 'Acme Corp');
    const actions = new ClientFormActions();
    
    const newState = actions.createClient(formState);
    
    expect(newState.client).toBeNull();
    expect(newState.error).toBe('Client ID cannot be empty');
  });

  it('should clear error when updating fields', () => {
    const formState = new ClientFormState('', '', null, 'Previous error');
    const actions = new ClientFormActions();
    
    const newState = actions.updateClientId(formState, 'new-id');
    
    expect(newState.error).toBe('');
  });

  it('should preserve other fields when updating', () => {
    const formState = new ClientFormState(
      'original-id',
      'Original Brand',
      null,
      'Some error'
    );
    const actions = new ClientFormActions();
    
    const newState = actions.updateBranding(formState, 'New Brand');
    
    expect(newState.clientId).toBe('original-id');
    expect(newState.branding).toBe('New Brand');
    expect(newState.error).toBe('');
  });
});