import requests
import subprocess
import json
import logging

# Initialize logger
logger = logging.getLogger("username_lookup")
logging.basicConfig(level=logging.DEBUG)

def lookup_username(username, platforms):
    """
    Lookup a username across multiple platforms using Sherlock.

    Args:
        username (str): The username to search for.
        platforms (list): A list of platforms to search on.

    Returns:
        dict: A dictionary with platform names as keys and URLs as values.
    """
    results = {}

    try:
        # Run Sherlock as a subprocess
        command = ["sherlock", username, "--print-found"]
        logger.debug(f"Running command: {' '.join(command)}")
        process = subprocess.run(command, capture_output=True, text=True)

        if process.returncode == 0:
            logger.debug("Sherlock executed successfully.")
            # Parse Sherlock's output
            for line in process.stdout.splitlines():
                logger.debug(f"Processing line: {line}")
                for platform in platforms:
                    if platform in line:
                        results[platform] = line.strip()
        else:
            logger.error(f"Sherlock error: {process.stderr.strip()}")
            results["error"] = process.stderr.strip()

    except Exception as e:
        logger.exception("Exception occurred during username lookup.")
        results["error"] = str(e)

    return results
