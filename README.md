# EFT-

## Resources:

- Twitchio documentation: https://twitchio.dev/en/dev-3.0/getting-started/quickstart.html

## FAQ

- How do I get the link for efttroll to be used in a stream:
- Code
```python
async def oauth() -> None:
    all_scopes = twitchio.Scopes.all()

    oauth = twitchio.authentication.OAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri="http://localhost:4343/oauth/callback",
        scopes=all_scopes  # Use updated kwargs
    )


    auth_url = oauth.get_authorization_url(force_verify=True)
    print(auth_url)
```
