import streamlit as st
from datetime import date
from PIL import Image
import io
import os
import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import base64
import json

# Load environment variables from .env file
load_dotenv()

# Retrieve values from .env
firebase_credentials_path = os.getenv('FIREBASE_CREDENTIALS_PATH')
database_url = os.getenv('DATABASE_URL')
storage_bucket = os.getenv('STORAGE_BUCKET')

# Initialize Firebase app
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_credentials_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': database_url,
        'storageBucket': storage_bucket
    })

class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.brokers = []
        self.brokers2 = []
        self.strategies = []


def get_session_state():
    if "session_state" not in st.session_state:
        st.session_state["session_state"] = SessionState()
    return st.session_state["session_state"]


def register_page():
    # Initialize or retrieve session state
    session_state = get_session_state()

    # Set the title for the Streamlit app
    st.markdown("<h3 style='color: darkblue'>Register</h3>",
                unsafe_allow_html=True)

    # Take inputs for client information
    name = st.text_input("Name:", key="name_input")
    UserName = st.text_input("Username:", key="Username_input")
    email = st.text_input("Email:", key="email_input")
    Password = st.text_input(
        "Password:", type="password", key="Password_input")
    phone = st.text_input("Phone Number:", key="phone_input")
    dob = st.date_input("Date of Birth:", min_value=date(
        1950, 1, 1), key="dob_input").strftime("%d-%m-%Y")
    aadhar = st.text_input("Aadhar Card No:", key="aadhar_input")
    pan = st.text_input("Pan Card No:", key="pan_input")
    bank_name = st.text_input("Bank Name:", key="bank_name_input")
    bank_account = st.text_input("Bank Account No:", key="bank_account_input")
    profile_picture = st.file_uploader(
        "Profile Picture", type=["png", "jpg", "jpeg"], key="profile_picture_input")

    # Add a header for the brokers section
    st.subheader("Brokers")

    # Add a button to allow addition of new broker details
    add_broker_1 = st.button("Add Broker 1")
    if add_broker_1:
        # Only add a new broker field if the last one is filled
        if len(session_state.brokers) == 0 or any(session_state.brokers[-1].values()):
            session_state.brokers.append({})

    # Create dynamic input fields for broker information
    broker_list_1 = []
    for i, broker_1 in enumerate(session_state.brokers):
        broker_name = st.selectbox(
            "Broker Name", ["Zerodha", "AliceBlue"], key=f"broker_name_{i}")
        broker_1["broker_name"] = broker_name
        broker_1["user_name"] = st.text_input(
            "User Name:", key=f"user_name_{i}")
        broker_1["password"] = st.text_input("Password:", key=f"password_{i}")
        broker_1["two_fa"] = st.text_input("2FA:", key=f"two_fa_{i}")
        broker_1["totp_auth"] = st.text_input(
            "TotpAuth:", key=f"totp_auth_{i}")
        broker_1["api_key"] = st.text_input("ApiKey:", key=f"api_key_{i}")
        broker_1["api_secret"] = st.text_input(
            "ApiSecret:", key=f"api_secret_{i}")
        broker_1["active"] = st.checkbox("Active:", key=f"active_{i}")
        broker_1["capital"] = st.number_input("Capital:", key=f"capital_{i}")
        broker_1["risk_profile"] = st.text_input(
            "Risk profile:", key=f"risk_profile_{i}")

        broker_list_1.append(broker_1)

    add_broker_2 = st.button("Add Broker 2")
    if add_broker_2:
        # Only add a new broker field if the last one is filled
        if len(session_state.brokers2) == 0 or any(session_state.brokers2[-1].values()):
            session_state.brokers2.append({})

    # Create dynamic input fields for broker information
    broker_list_2 = []
    for i, broker_2 in enumerate(session_state.brokers2):
        # Determine the options for the second broker based on the selection of the first broker
        broker_1_selection = session_state.brokers[i]["broker_name"]
        broker_name_options = [
            "AliceBlue"] if broker_1_selection == "Zerodha" else ["Zerodha"]

        broker_name = st.selectbox(
            "Broker Name", broker_name_options, key=f"broker_name2_{i}")
        broker_2["broker_name"] = broker_name
        broker_2["user_name"] = st.text_input(
            "User Name:", key=f"user_name2_{i}")
        broker_2["password"] = st.text_input("Password:", key=f"password2_{i}")
        broker_2["two_fa"] = st.text_input("2FA:", key=f"two_fa2_{i}")
        broker_2["totp_auth"] = st.text_input(
            "TotpAuth:", key=f"totp_auth2_{i}")
        broker_2["api_key"] = st.text_input("ApiKey:", key=f"api_key2_{i}")
        broker_2["api_secret"] = st.text_input(
            "ApiSecret:", key=f"api_secret2_{i}")
        broker_2["active"] = st.checkbox("Active:", key=f"active2_{i}")
        broker_2["capital"] = st.number_input("Capital:", key=f"capital2_{i}")
        broker_2["risk_profile"] = st.text_input(
            "Risk profile:", key=f"risk_profile2_{i}")

        broker_list_2.append(broker_2)

    st.subheader("Strategies Subscribed")

    # Add a button to allow addition of new strategy details
    add_strategy = st.button("Add Strategy")
    if add_strategy:
        # Only add a new strategy field if the last one is filled
        if len(session_state.strategies) == 0 or any(session_state.strategies[-1].values()):
            session_state.strategies.append({})

    # Create dynamic input fields for strategy information
    strategy_list = []
    all_strategies = ["AmiPy", "MP Wizard", "ZRM",
                      "Overnight Options", "Screenipy Stocks"]
    for i, strategy in enumerate(session_state.strategies):
        strategy["strategy_name"] = st.multiselect(
            "Strategy Name", all_strategies, key=f"strategy_name_{i}")
        strategy["broker"] = st.multiselect(
            "Broker", ["Zerodha", "AliceBlue"], key=f"strategy_broker_name_{i}")

        selected_strategies = strategy["strategy_name"]
        selected_broker = strategy["broker"]

        for selected_strategy in selected_strategies:
            for selected_broker_name in selected_broker:
                perc_allocated_key = f"strategy_perc_allocated_{selected_strategy}_{selected_broker_name}_{i}"
                strategy[perc_allocated_key] = st.selectbox(f"Percentage Allocated for {selected_strategy} and {selected_broker_name} (%):", options=[
                                                            f"{i/10:.1f}%" for i in range(0, 101)], key=f"strategy_perc_allocated_{selected_strategy}_{selected_broker_name}_{i}")

        strategy_list.append({
            "strategy_name": selected_strategies,
            "broker": selected_broker,
            **strategy
        })
    # Take input for comments
    comments = st.text_area("Comments:", key="comments_input")

    smart_contract = st.text_area("Smart Contract", key="smart_contract_input")

    # Add a submit button
    submit = st.button("Submit", key="submit_button")

    # Check if the submit button is clicked
    if submit:
        # Check if all the fields are filled before submitting
        if name and dob and phone and email and aadhar and pan and bank_account and broker_list_1 and strategy_list:
            # Validate PAN Card Number (should be in uppercase)
            pan = pan.upper()

        # Validate Phone Number (should be 10 digits)
            if len(phone) != 10:
                st.error("Phone Number should be 10 digits")
                return

        # Validate Aadhaar Card Number (should be 12 digits)
            if len(aadhar) != 12:
                st.error("Aadhaar Card No should be 12 digits")
                return
                # Create a list with all the client data
            client_data = [name, UserName, email, Password, phone, dob, aadhar, pan,
                           bank_name, bank_account, broker_list_1, broker_list_2, strategy_list, comments, smart_contract]

            # Save the uploaded profile picture as binary data if it exists
            if profile_picture is not None:
                # Open the image using PIL
                image = Image.open(profile_picture)

                # Create a BytesIO object to hold the image data
                image_bytes = io.BytesIO()

                # Save the image to the BytesIO object
                image.save(image_bytes, format=image.format)

                # Encode the image bytes to a Base64 string
                image_base64 = base64.b64encode(
                    image_bytes.getvalue()).decode("utf-8")

                # Add the image base64 string to the client list
                client_data.append(image_base64)

            # Convert client data to dictionary for firebase compatibility
            client_data_dict = {
                "Name": client_data[0],
                "Username": client_data[1],
                "Email": client_data[2],
                "Password": client_data[3],
                "Phone Number": client_data[4],
                "Date of Birth": client_data[5],
                "Aadhar Card No": client_data[6],
                "PAN Card No": client_data[7],
                "Bank Name": client_data[8],
                "Bank Account No": client_data[9],
                "Brokers list 1": client_data[10],
                "Brokers list 2": client_data[11],
                "Strategy list": client_data[12],
                "Comments": client_data[13],
                "Smart Contract": client_data[14],
                "Profile Picture": client_data[15] if profile_picture is not None else None,
            }

            # Save the client data to Firebase Realtime Database
            try:
                # Get a reference to the 'clients' node in the database
                ref = db.reference('clients')

                # Use the client name as the client key
                client_key = name.lower().replace(" ", "_")

                # Save the client data under the client key
                ref.child(client_key).set(client_data_dict)

                # Show a success message
                st.success("Client data saved successfully!")
            except Exception as e:
                # Show an error message if there's an exception
                st.error("Failed to save client data: " + str(e))
        else:
            # If not all fields are filled, show an error message
            unfilled_fields = []
            if not name:
                unfilled_fields.append("Name")
            if not dob:
                unfilled_fields.append("Date of Birth")
            if not phone:
                unfilled_fields.append("Phone Number")
            if not email:
                unfilled_fields.append("Email")
            if not aadhar:
                unfilled_fields.append("Aadhar Card No")
            if not pan:
                unfilled_fields.append("Pan Card No")
            if not bank_account:
                unfilled_fields.append("Bank Account No")
            if not broker_list_1:
                unfilled_fields.append("Brokers")
            if not strategy_list:
                unfilled_fields.append("Strategies Subscribed")

            error_message = "Please fill the following fields: " + \
                ", ".join(unfilled_fields)
            st.error(error_message)
                
    # Function to save data to broker.json file
    def save_to_json(data):
        with open('broker.json', 'w') as file:
            json.dump(data, file, indent=4)
        st.success("Data saved successfully to broker.json!")

    # Assuming you've already set up Streamlit and collected all the relevant inputs
    # These inputs would include the details for brokers in broker_list_1 and broker_list_2

    data_to_save = {}

    # Processing Zerodha broker details
    for broker_1 in broker_list_1:
        if broker_1["broker_name"] == "Zerodha":
            username = broker_1["user_name"]
            data_to_save["zerodha"] = {
                username: {
                    "username": username,
                    "password": broker_1["password"],
                    "api_key": broker_1["api_key"],
                    "api_secret": broker_1["api_secret"],
                    "totp": broker_1.get("totp_auth", ""),
                    "access_token": "",
                    "mobile_number": phone,
                    "percentageRisk": {
                        "AmiPy": broker_1.get("AmiPy", 0),
                        "MPWizard": broker_1.get("MPWizard", 0),
                        "ZRM": broker_1.get("ZRM", 0),
                        "overnight_option": broker_1.get("overnight_option", 0)
                    },
                    "current_capital": broker_1.get("capital", 0),
                    "yesterday_PnL": 0,
                    "expected_morning_balance": 0
                }
            }

    # Processing AliceBlue broker details
    for broker_2 in broker_list_2:
        if broker_2["broker_name"] == "AliceBlue":
            username = broker_2["user_name"]
            data_to_save["aliceblue"] = {
                username: {
                    "username": username,
                    "password": broker_2["password"],
                    "twoFA": broker_2.get("two_fa", ""),
                    "api_secret": broker_2["api_secret"],
                    "app_code": "",
                    "api_key": broker_2["api_key"],
                    "totp_access": broker_2.get("totp_auth", ""),
                    "session_id": "",
                    "mobile_number": phone,
                    "percentageRisk": {
                        "AmiPy": broker_2.get("AmiPy", 0),
                        "MPWizard": broker_2.get("MPWizard", 0),
                        "overnight_option": broker_2.get("overnight_option", 0)
                    },
                    "current_capital": broker_2.get("capital", 0),
                    "yesterday_PnL": 0,
                    "expected_morning_balance": 0
                }
            }

    # Save the formatted data to broker.json when the user clicks the save button
    if st.button("Save to broker.json"):
        save_to_json(data_to_save)

if __name__ == "__main__":
    register_page()
