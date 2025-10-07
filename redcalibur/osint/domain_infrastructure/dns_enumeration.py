import dns.resolver

DEFAULT_NAMESERVERS = ["1.1.1.1", "8.8.8.8"]

def _resolver(nameservers=None, timeout=5.0):
    r = dns.resolver.Resolver(configure=True)
    r.timeout = float(timeout)
    r.lifetime = float(timeout)
    if nameservers:
        r.nameservers = nameservers
    return r

def enumerate_dns_records(domain: str, nameservers=None, timeout: float = 5.0):
    """
    Enumerate DNS records with resilient fallback resolvers.

    Args:
        domain: Domain to enumerate
        nameservers: Optional list of nameserver IPs to use
        timeout: Per-query timeout seconds

    Returns:
        dict[str, list|str]
    """
    record_types = ['A', 'AAAA', 'MX', 'TXT', 'CNAME', 'NS']
    dns_records = {}

    resolvers = []
    resolvers.append(_resolver(nameservers, timeout))
    # Fallback resolver with public resolvers if custom/system fails
    if not nameservers:
        resolvers.append(_resolver(DEFAULT_NAMESERVERS, timeout))

    for r in resolvers:
        try:
            # probe with A; if fails, try next resolver
            list(r.resolve(domain, 'A'))
            active = r
            break
        except Exception:
            active = None
    if active is None:
        # Report errors per record with a uniform message
        err = f"Name resolution failed for {domain}"
        for t in record_types:
            dns_records[t] = err
        return dns_records

    for record_type in record_types:
        try:
            answers = active.resolve(domain, record_type)
            dns_records[record_type] = [answer.to_text() for answer in answers]
        except Exception as e:
            dns_records[record_type] = str(e)

    return dns_records
