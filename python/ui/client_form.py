from dataclasses import dataclass
from typing import Optional
from python.domains.client import Client


@dataclass(frozen=True)
class ClientFormState:
    client_id: str = ""
    branding: str = ""
    client: Optional[Client] = None
    error: str = ""
    
    def is_valid(self) -> bool:
        return self.client_id.strip() != "" and self.branding.strip() != ""


class ClientFormActions:
    def update_client_id(self, state: ClientFormState, client_id: str) -> ClientFormState:
        return ClientFormState(
            client_id=client_id,
            branding=state.branding,
            client=state.client,
            error=""
        )
    
    def update_branding(self, state: ClientFormState, branding: str) -> ClientFormState:
        return ClientFormState(
            client_id=state.client_id,
            branding=branding,
            client=state.client,
            error=""
        )
    
    def create_client(self, state: ClientFormState) -> ClientFormState:
        try:
            if not state.client_id.strip():
                return ClientFormState(
                    client_id=state.client_id,
                    branding=state.branding,
                    client=None,
                    error="Client ID cannot be empty"
                )
            
            client_data = {
                'id': state.client_id,
                'branding': {
                    'name': state.branding,
                    'logo': '',
                    'primary_color': '#000000'
                }
            }
            client = Client(client_data)
            return ClientFormState(
                client_id=state.client_id,
                branding=state.branding,
                client=client,
                error=""
            )
        except Exception as e:
            return ClientFormState(
                client_id=state.client_id,
                branding=state.branding,
                client=None,
                error=str(e)
            )