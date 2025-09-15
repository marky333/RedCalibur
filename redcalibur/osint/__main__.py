from .whois_lookup import perform_whois_lookup, is_valid_domain
from .shodan_scan import perform_shodan_scan
from .social_media_scraper import scrape_social_media

def main():
    print("Welcome to the OSINT module of RedCalibur!")
    print("1. WHOIS Lookup")
    print("2. Shodan Scan")
    print("3. Social Media Scraper")

    choice = input("Enter your choice (1/2/3): ")

    if choice == "1":
        domain = input("Enter the domain name for WHOIS lookup: ")
        if is_valid_domain(domain):
            result = perform_whois_lookup(domain)
            print("WHOIS Lookup Result:")
            print(result)
        else:
            print("Invalid domain name. Please try again.")

    elif choice == "2":
        api_key = input("Enter your Shodan API key: ")
        target = input("Enter the target IP or domain for Shodan scan: ")
        if api_key and target:
            result = perform_shodan_scan(api_key, target)
            print("Shodan Scan Result:")
            print(result)
        else:
            print("API key and target are required.")

    elif choice == "3":
        platform = input("Enter the social media platform (e.g., 'twitter', 'instagram'): ")
        username = input("Enter the username to scrape: ")
        if platform and username:
            result = scrape_social_media(platform, username)
            print("Social Media Scraper Result:")
            print(result)
        else:
            print("Platform and username are required.")

    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
