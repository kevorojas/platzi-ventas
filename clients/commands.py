from tabulate import tabulate
import click
from click.termui import prompt
from clients.services import ClientServices
from clients.models import Client


@click.group()
def clients():
    """Manages the clients lifecycle
    """
    pass


@clients.command()
@click.option('-n', '--name', type=str, prompt=True, help='The clien\'s name')
@click.option('-c', '--company', type=str, prompt=True, help='The client\'s company')
@click.option('-e', '--email', type=str, prompt=True, help='The client\'s email')
@click.option('-p', '--position', type=str, prompt=True, help='The client\'s position')
@click.pass_context
def create(ctx, name, company, email, position):
    """Create a client

    Args:
        ctx (dictionary): object context
        name (string): name of the client
        company (string): company of the client
        email (string): email of the client
        position (string): [position of the client
    """
    client = Client(name, company, email, position)
    client_service = ClientServices(ctx.obj['clients_table'])
    client_service.create_client(client)


@clients.command()
@click.pass_context
def list(ctx):
    """list clients

    Args:
        ctx (dictionary): object context
    """
    clients_service = ClientServices(ctx.obj['clients_table'])
    clients_list = clients_service.list_clients()

    headers = [field.capitalize() for field in Client.schema()]
    table = []

    for client in clients_list:
        table.append([
            client['name'],
            client['company'],
            client['email'],
            client['position'],
            client['uid'],
        ])
    
    click.echo(tabulate(table, headers))


@clients.command()
@click.argument('client_uid')
@click.pass_context
def update(ctx, client_uid):
    """Update a client

    Args:
        ctx (dictionary): object context
        client_uid (string): client uid
    """
    client_service = ClientServices(ctx.obj['clients_table'])
    client_list = client_service.list_clients()

    client = [client for client in client_list if client['uid'] == client_uid]
    if client:
        client = _update_client_flow(Client(**client[0]))
        client_service.update_client(client)
        
        click.echo('Client updated')
    else:
        click.echo('Client not found')

def _update_client_flow(client):
    click.echo('Leave empty if you dont want to modify the value')

    client.name = click.prompt('New name', type=str, default=client.name)
    client.company = click.prompt('New company', type=str, default=client.company)
    client.email = click.prompt('New email', type=str, default=client.email)
    client.position = click.prompt('New position', type=str, default=client.position)

    return client


@clients.command()
@click.argument('client_uid')
@click.pass_context
def delete(ctx, client_uid):
    """Delete a client

    Args:
        ctx (dictionary): object context
        client_uid (string): client uid
    """
    client_service = ClientServices(ctx.obj['clients_table'])
    if click.confirm(f'Are you sure yo want to delete the client whit uid: {client_uid}'):
        client_service.delete_client(client_uid)
        

all = clients
