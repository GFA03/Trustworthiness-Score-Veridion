import companyReviews
import pandas as pd
import os
import Location_Revenue_EmpCount_Relation
import scrap_linkedin
import utils
import keywords_in_site
import FileWriter


def main():
    dfs = []

    for fileName in os.listdir("datasets/"):
        if fileName.endswith('.parquet'):
            df = pd.read_parquet(os.path.join("datasets", fileName))
            dfs.append(df)

    file = pd.concat(dfs, ignore_index=True)
    file = file.sample(frac=1).reset_index(drop=True)
    fileWrite = FileWriter.FileWriter("score.txt")
    i = 0
    for ind in file.index:
        i += 1
        print(i)
        if i == 200:
            break
        score = 0

        (domain, name, legal_name, year_founded, phones, revenue, industry, email, location_number, website,
         employee_count, keywords, linkedin, youtube, twitter, facebook, instagram) = \
            file["domain"][ind], file["name"][ind], file["legal_name"][ind], file["year_founded"][ind], \
            file["all_phones"][ind], file["revenue"][ind], file["agg_industry"][ind], \
            file["all_emails"][ind], file["location_number"][ind], file["website_url"][ind], \
            file["employee_count"][ind], file["keywords"][ind], file["linkedin"][ind], file["youtube"][ind], \
            file["twitter"][ind], file["facebook"][ind], file["instagram"][ind]
        #  Test 1: Google Maps Review System
        # To work you should get an Google Maps API key with Placing API
        # score += companyReviews.get_company_reviews(name, api_key) * 0.25

        # Test 2: Correlation between Revenue, Domain, Locations number and Employee Count through Linear Regression
        score += Location_Revenue_EmpCount_Relation.scoreCalculation(industry, revenue, location_number,
                                                                     employee_count) * 0.15

        # Test 3: Data scrapping Linkedin (Followers + Last recently post)
        score += scrap_linkedin.scrap_linkedin(linkedin) * 0.2

        # Test 4: Social Activity
        score += utils.socialMediaNumber(facebook, instagram, twitter, linkedin, youtube) * 0.15

        # Test 5: Count of phones and emails
        score += utils.countPhones(phones) * 0.05
        score += utils.countEmails(email) * 0.05

        # Test 6: Keyworkds on company's website main page
        score += keywords_in_site.keywords_in_site(website, keywords) * 0.05

        # Test 7: http Secure check
        score += utils.urlChecker(website) * 0.10
        fileWrite.write_to_file(f"Company name: {name.capitalize()}\nScore: {score}\n\n")


if __name__ == '__main__':
    main()
