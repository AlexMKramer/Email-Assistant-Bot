# Email Assistant Python Application

## Overview

This Python application is an Email Assistant that connects to your IMAP server, reads unread emails from the INBOX, and generates responses using an external language model. It also sends responses to the original senders. The application uses the `imapclient`, `email`, `smtplib`, and `requests` libraries.

This application was built primarily for MacBooks, as that is all I have to test it on.  Running LLMs on a MacBook with high memory is a good way to run them locally.  I am not aware of the Windows/Linux app equivelants to Ollama, but I dont see why this couldnt be adapted to fit other platforms.

I made this as a fun experiment, I don't recommend having this run automatically, or with any important emails that come in.  Use at your own risk.

## Features

- **Read Unread Emails:** The application connects to the IMAP server and retrieves unread emails from the INBOX.

- **Generate Responses:** It uses an external language model to generate responses based on the content of the received emails.

- **Send Responses:** The generated responses are sent back to the original senders using the SMTP server.

## Prerequisites

Before running the application, ensure you have the following:

- Python installed on your machine.
- Required Python libraries installed (`imapclient`, `email`, `smtplib`, `requests`).
- Ollama's External language model server running locally at `http://localhost:11434/api/generate`.
- Environment variables set with your email credentials (`username`, `username_email_address`, `password`, `email_address`).

## Usage

1. Clone the repository:

    ```bash
    git clone https://github.com/your/repository.git
    ```

2. Install dependencies:

    ```bash
    pip install imapclient email smtplib requests python-dotenv
    ```

3. Set up environment variables:

     Edit the `.env` file in the root directory and add the following:

    ```dotenv
    USERNAME=your_username
    USERNAME_EMAIL_ADDRESS=your_username_email_address
    PASSWORD=your_password
    EMAIL_ADDRESS=your_email_address
    ```

    With Apple's custom domain email addresses, it can be confusing to discern which address goes where.

   Username is usually your email address associated with your iCloud account, minus the domain.  So if your address is example@icloud.com, enter 'example'.
   
   Username_email_address will be the full address: example@icloud.com

   Password should be an App Specific Password generated on Apple's site: https://support.apple.com/kb/HT204397

   Email_address will be the address you want the email to be sent from.

   This is all laid out seperately to make it so you can use your own domain address through Apple's cloud service.  I have my own custom domain, so the setup looks like this:
   ```
    USERNAME=example
    USERNAME_EMAIL_ADDRESS=example@gmail.com
    PASSWORD=PASSWORD
    EMAIL_ADDRESS=example@customdomain.org
   ```

5. Create the Ollama model:
    ```bash
    ollama create emailAssistant -f ./Modelfile
    ```
    
6. Run the application:

    ```bash
    python main.py
    ```

## Customization

- **SMTP Server:** Update the `smtp_server_address` variable with your SMTP server address.
- **Subject Prefix:** Modify the `subject` variable in the `respond_to_email` function to change the subject prefix of the response emails.
- **Response Prompt:** Customize the `prompt` variable in the `generate` function to alter the prompt for generating responses.

## Important Note

Make sure to handle your email credentials securely and avoid hardcoding them directly in the source code.

## Acknowledgments

This application utilizes the `requests` library to interact with an external language model for response generation.

## License

This project is licensed under the [MIT License](LICENSE).
