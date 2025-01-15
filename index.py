import csv
import json
import typer
from typing_extensions import Annotated
from helpers.helper import csv_to_json, check_user_membership
from apis.snykApi import add_member_to_snyk_organization, get_snyk_orgs, get_pending_user_list, get_group_memberships

app = typer.Typer()
    
    
@app.command()
def accept_user_pending_invite(group_id: Annotated[str, typer.Argument(help="Original group ID in Snyk")]):
    # Store for users that can not be added to an organization
    user_data = []
    # Gather orgs from provided group id
    print("Collecting organization IDs")
    orgs_data = get_snyk_orgs(group_id)
    # Gather user group membership list
    user_group_members_data = get_group_memberships(group_id)
    
    # loop through org data
    for org_data in orgs_data:
        # Gather pending invite list
        print(f"Collecting pending invite list for {org_data['attributes']['name']}")
        pending_users_list = get_pending_user_list(org_data['id'])
        print(f"Found {len(pending_users_list)} pending users {json.dumps(pending_users_list, indent=4)}")
        
        # if there are pending users and user org memberships, loop through pending users and check if they have an org/group membership
        if any(pending_users_list) and any(user_group_members_data):
            for pending_user in pending_users_list:
                user_email = pending_user['attributes']['email']
                
                if check_user_membership(user_email, user_group_members_data):
                    user_name = user_group_members_data['relationships']['user']['data']['attributes']['name']
                    org_name = org_data['attributes']['name']
                    org_id = org_data['id']
                    
                    print(f"User {user_email} already has an group membership. Adding {user_name} to {org_name}")
                    add_member_to_snyk_organization(group_id, org_id, pending_user['attributes']['id'], pending_user['attributes']['role'])
                else:
                    user_data.append({
                        'email': user_email,
                        'org_id': org_id,
                        'org_name': org_name
                    })
                    print(f"User {user_email} does not have an group membership but has an existing pending invite.  Can not add user to group.")
        if pending_users_list and not user_group_members_data:
            for pending_user in pending_users_list:
                user_data.append({
                    'email': pending_user['attributes']['email'],
                    'org_id': org_data['id'],
                    'org_name': org_data['attributes']['name']
                })
            
    
    # Save collected data to CSV
    if user_data:
        csv_filename = 'failed_to_add_user_memberships.csv'
        fieldnames = ['email', 'org_id', 'org_name']
        
        try:
            with open(csv_filename, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(user_data)
                print(f"\nUser data has been saved to {csv_filename}")
        except Exception as e:
            print(f"Error saving user data to CSV: {e}")

if __name__ == "__main__":
    app()