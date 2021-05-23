import csv
from clients.models import Client
import os


class ClientServices():
    def __init__(self, table_name):
        self.table_name = table_name

    def create_client(self, client):
        with open(self.table_name, mode='a') as f:
            writer = csv.DictWriter(f, fieldnames=Client.schema())
            writer.writerow(client.to_dict())

    def list_clients(self):
        with open(self.table_name, mode='r') as f:
            reader = csv.DictReader(f, fieldnames=Client.schema())
            return list(reader)

    def update_client(self, updated_client):
        clients = self.list_clients()

        updated_clients = []
        for client in clients:
            if client['uid'] == updated_client.uid:
                updated_clients.append(updated_client.to_dict())
            else:
                updated_clients.append(client)
        self._save_to_disk(updated_clients)

    def delete_client(self, client_uid):
        list_clients = self.list_clients()

        list_clients_updated = []
        for client in list_clients:
            if client['uid'] != client_uid:
                list_clients_updated.append(client)
                
        self._save_to_disk(list_clients_updated)           

        
    def _save_to_disk(self, clients):
        tmp_table_name = f'{self.table_name}.tmp'
        with open(tmp_table_name, mode='w') as f:
            writer = csv.DictWriter(f, fieldnames=Client.schema())
            writer.writerows(clients)

        os.rename(self.table_name, self.table_name + '.old')
        os.rename(tmp_table_name, self.table_name)
        os.remove(self.table_name + '.old')
