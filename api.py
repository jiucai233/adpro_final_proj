import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient.discovery
import googleapiclient.errors

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1vM2UylvCuIcBQrWf8p_xiGE0sNdpg1_XgwT2VOjrQIg"


def authenticate():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret_966889279952-k86ftn0fjuo9psh3ko6qt6k95hqn7cfr.apps.googleusercontent.com.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())
    return creds

def append_to_sheet(spreadsheet_id, range_name, values):
    creds = authenticate()
    service = googleapiclient.discovery.build('sheets', 'v4', credentials=creds)
    body = {
        'values': [values]
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, 
        range=range_name,
        valueInputOption="USER_ENTERED",
        body=body
    ).execute()
    return result

def get_data_from_sheet(spreadsheet_id, range_name):
    creds = authenticate()
    service = googleapiclient.discovery.build('sheets', 'v4', credentials=creds)
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    return result.get('values', [])


if __name__ == '__main__':
    append_to_sheet('1vM2UylvCuIcBQrWf8p_xiGE0sNdpg1_XgwT2VOjrQIg', 'A2:C2', ['2023-06-04', '식비', '10000'])
    data = get_data_from_sheet('1vM2UylvCuIcBQrWf8p_xiGE0sNdpg1_XgwT2VOjrQIg', 'A2:C2')
    print(data)
