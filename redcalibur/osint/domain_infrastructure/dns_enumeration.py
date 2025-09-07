import dns.resolver

def enumerate_dns_records(domain):
    """
    Enumerate DNS records for the given domain.

    Args:
        domain (str): The domain name to enumerate.

    Returns:
        dict: A dictionary containing DNS records.
    """
    record_types = ['A', 'AAAA', 'MX', 'TXT', 'CNAME', 'NS']
    dns_records = {}

    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            dns_records[record_type] = [answer.to_text() for answer in answers]
        except Exception as e:
            dns_records[record_type] = str(e)

    return dns_records
