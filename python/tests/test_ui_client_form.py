import pytest
from python.ui.client_form import ClientFormState, ClientFormActions
from python.domains.client import Client


def test_should_initialize_with_empty_form_state():
    form_state = ClientFormState()
    
    assert form_state.client_id == ""
    assert form_state.branding == ""
    assert form_state.client is None
    assert form_state.error == ""
    assert form_state.is_valid() is False


def test_should_update_client_id():
    form_state = ClientFormState()
    actions = ClientFormActions()
    
    new_state = actions.update_client_id(form_state, "test-client-123")
    
    assert new_state.client_id == "test-client-123"
    assert new_state.branding == ""
    assert new_state.error == ""


def test_should_update_branding():
    form_state = ClientFormState()
    actions = ClientFormActions()
    
    new_state = actions.update_branding(form_state, "Acme Corp")
    
    assert new_state.branding == "Acme Corp"
    assert new_state.client_id == ""
    assert new_state.error == ""


def test_should_validate_form_when_both_fields_filled():
    form_state = ClientFormState(client_id="test-123", branding="Acme")
    
    assert form_state.is_valid() is True


def test_should_not_validate_form_when_client_id_empty():
    form_state = ClientFormState(client_id="", branding="Acme")
    
    assert form_state.is_valid() is False


def test_should_not_validate_form_when_branding_empty():
    form_state = ClientFormState(client_id="test-123", branding="")
    
    assert form_state.is_valid() is False


def test_should_create_client_successfully():
    form_state = ClientFormState(client_id="test-123", branding="Acme Corp")
    actions = ClientFormActions()
    
    new_state = actions.create_client(form_state)
    
    assert new_state.client is not None
    assert new_state.client.id == "test-123"
    assert new_state.client.branding.name == "Acme Corp"
    assert new_state.error == ""


def test_should_handle_client_creation_error():
    form_state = ClientFormState(client_id="", branding="Acme Corp")
    actions = ClientFormActions()
    
    new_state = actions.create_client(form_state)
    
    assert new_state.client is None
    assert new_state.error == "Client ID cannot be empty"


def test_should_clear_error_when_updating_fields():
    form_state = ClientFormState(error="Previous error")
    actions = ClientFormActions()
    
    new_state = actions.update_client_id(form_state, "new-id")
    
    assert new_state.error == ""


def test_should_preserve_other_fields_when_updating():
    form_state = ClientFormState(
        client_id="original-id",
        branding="Original Brand",
        error="Some error"
    )
    actions = ClientFormActions()
    
    new_state = actions.update_branding(form_state, "New Brand")
    
    assert new_state.client_id == "original-id"
    assert new_state.branding == "New Brand"
    assert new_state.error == ""