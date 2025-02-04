import csv
import json
import typer
from typing_extensions import Annotated
from apis.snykApi import add_member_to_snyk_organization, get_snyk_orgs, get_pending_user_list

app = typer.Typer()
    
    
@app.command()
def accept_user_pending_invite(group_id: Annotated[str, typer.Argument(help="Original group ID in Snyk")]):
    # Store for users that can not be added to an organization
    failed_user_data = []
    # Gather orgs from provided group id
    print("Collecting organization IDs")
    orgs_data = get_snyk_orgs(group_id)
    
    # loop through org data
    for org_data in orgs_data:
        # Set the org id and name
        org_id = org_data['id']
        org_name = org_data['attributes']['name']
        # Gather pending invite list
        print(f"Collecting pending invite list for {org_data['attributes']['name']}")
        pending_users_list = get_pending_user_list(org_data['id'])
        print(f"Found {len(pending_users_list)} pending users {json.dumps(pending_users_list, indent=4)}")
        
        # if there are pending users, loop through pending users and try to invite them to the snyk organization
        if any(pending_users_list):
            for pending_user in pending_users_list:
                user_email = pending_user['attributes']['email']
                add_member_success = add_member_to_snyk_organization(group_id, org_id, pending_user['attributes']['id'], pending_user['attributes']['role'])
                if len(add_member_success) == 1:
                    print(f"User {user_email} added to {org_name}")
                else:
                    failed_user_data.append({
                        'email': user_email,
                        'org_id': org_id,
                        'org_name': org_name,
                        'error': add_member_success[1]
                    })
                    print(f"Failed to add {user_email} to {org_name}.  Error: {add_member_success[1]}")
    
    # Save collected data to CSV
    if failed_user_data:
        csv_filename = 'failed_to_add_user_memberships.csv'
        fieldnames = ['email', 'org_id', 'org_name', 'error']
        
        try:
            with open(csv_filename, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(failed_user_data)
                print(f"\nUser data has been saved to {csv_filename}")
        except Exception as e:
            print(f"Error saving user data to CSV: {e}")

if __name__ == "__main__":
    app()