import requests
from bs4 import BeautifulSoup
import re


def fetch_movie_details(movie_name):
    """
    Fetch movie details from Douban based on the movie name.

    Parameters:
        movie_name (str): The name of the movie to search.

    Returns:
        dict: A dictionary containing movie details or error messages.
    """
    search_url = f"https://www.douban.com/search?cat=1002&q={movie_name}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Referer": "https://www.douban.com",
    }

    try:
        # Fetch the search results page
        response = requests.get(search_url, headers=headers)

        if response.status_code != 200:
            return {
                "error": f"Search request failed with status code: {response.status_code}"
            }

        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("div", class_="result")

        for result in results:
            title_tag = result.find("a")
            if title_tag:
                title = title_tag["title"]
                initial_link = title_tag["href"]
                # if title not in movie_name and movie_name not in title:
                #     continue

                # Follow the initial detail link
                jump_response = requests.get(initial_link, headers=headers)
                if jump_response.status_code != 200:
                    return {
                        "error": f"Failed to fetch jump page: {jump_response.status_code}"
                    }

                jump_soup = BeautifulSoup(jump_response.text, "html.parser")
                script_tag = jump_soup.find("script")

                if script_tag:
                    match = re.search(
                        r"window\.location\.replace\('(.+?)'\)", script_tag.string
                    )
                    if match:
                        final_link = match.group(1)

                        # Access the final detail page
                        detail_response = requests.get(final_link, headers=headers)
                        if detail_response.status_code != 200:
                            return {
                                "error": f"Failed to fetch final detail page: {detail_response.status_code}"
                            }

                        detail_soup = BeautifulSoup(detail_response.text, "html.parser")

                        try:
                            name = detail_soup.find(
                                "span", property="v:itemreviewed"
                            ).get_text(strip=True)
                            year = detail_soup.find("span", class_="year").get_text(
                                strip=True
                            )
                            summary = detail_soup.find(
                                "span", property="v:summary"
                            ).get_text(strip=True)
                            info_section = detail_soup.find("div", id="info").get_text()

                            return {
                                "name": name,
                                "year": year,
                                "summary": summary,
                                "info": info_section,
                            }

                        except AttributeError:
                            return {
                                "error": "Some movie details are missing, possibly due to a changed webpage structure."
                            }

                    else:
                        return {"error": "No redirect link found on jump page."}
                else:
                    return {"error": "No redirect script found on jump page."}

        return {"error": "Movie not found in search results."}

    except requests.RequestException as e:
        return {"error": f"An error occurred during the request: {e}"}


# Example usage
# if __name__ == "__main__":
#     movie_name = "白夜破晓"
#     movie_details = fetch_movie_details(movie_name)
#     print(movie_details)
