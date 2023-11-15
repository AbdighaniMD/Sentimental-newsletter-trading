# **Sentimental newsletter trading**

## language Tech

**Server:** Python

# About
- Leveraging Reddit data to identify trending stocks and extract valuable insights by using openai API summary.

## UML Diagram
- Email reports to deliver the most relevant and up-to-date information about trending stock Subscribers.

![UML Diagram](./asset/emailReport.jpeg)


## Environment Variables
In order to Start up the project, create venv and file env.py with these variables, with your own values.

**Reddit API**
`REDDIT_CLIENT_IDenv`
`REDDIT_CLIENT_SECRETenv` 
`REDDIT_USERNAMEenv` 
`REDDIT_PASSWORDenv` 
`REDDIT_USER_AGENTenv` 

**openai API**
`GPT_SECRET_KEYenv` 

**Gmail settup**
`MAIL_SMTP_SERVERenv`
`MAIL_SMTP_PORTenv`
`MAIL_SMTP_USERNAMEenv`
`MAIL_SMTP_PASSWORDenv`
`MAIL_DISPLAY_NAMEenv`

**AWS Settup**
`AWS_S3_BUCKET_NAMEenv`
`AWS_REGIONenv`
`AWS_ACCESS_KEYenv`
`AWS_SECRET_KEYenv`

## Run Locally

Clone the project

```bash
  git clone https://github.com/AbdighaniMD/Sentimental-newsletter-trading.git
```

Install dependencies

```bash
  pip install -r requirement.txt
```

Start the server

```bash
  python main.py
```


## Author

- [@AbdighaniMD](https://github.com/AbdighaniMD)