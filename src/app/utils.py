from app.models.socials import SocialAccount, SocialNetwork


def get_account_url(network: SocialNetwork, account: SocialAccount) -> str:
    """
    Returns URL to access social account on network
    """
    return f"https://{network.domain}{network.account_prefix}{account.username}"
