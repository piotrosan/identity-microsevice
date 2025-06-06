import os

if not os.getenv('mail_password'):
    raise ValueError('Set mail password env variable')

if not os.getenv('mail_username'):
    raise ValueError('Set mail username env variable')

if not os.getenv('mail_from'):
    raise ValueError('Set mail from env variable')

if not os.getenv('token_exp_time'):
    raise ValueError('Set token exp time env variable')

if not os.getenv('token_exp_delta'):
    raise ValueError('Set token exp delta env variable')

if not os.getenv('refresh_token_exp_time'):
    raise ValueError('Set refresh token exp time env variable')

if not os.getenv('refresh_token_exp_delta'):
    raise ValueError('Set refresh token exp delta env variable')

if not os.getenv('hs_key'):
    raise ValueError('Set hs key env variable')
