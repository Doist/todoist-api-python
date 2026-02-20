# Authentication

This module provides helpers to authenticate with Todoist using OAuth.

## Quick start

```python
import uuid

from todoist_api_python.authentication import get_auth_token, get_authentication_url

# 1. Generate a random state
state = str(uuid.uuid4())

# 2. Build the authorization URL
url = get_authentication_url(
    client_id="YOUR_CLIENT_ID",
    scopes=["data:read", "task:add"],
    state=state,
)

# 3. Redirect the user to `url`
# 4. Handle the OAuth callback and obtain the auth code
code = "CODE_YOU_OBTAINED"

# 5. Exchange code for an access token
auth_result = get_auth_token(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    code=code,
)

# 6. Ensure state is consistent, and done!
assert auth_result.state == state
access_token = auth_result.access_token
```

For detailed implementation steps and security considerations, refer to the [Todoist OAuth documentation](https://todoist.com/api/v1/docs#tag/Authorization/OAuth).

::: todoist_api_python.authentication
