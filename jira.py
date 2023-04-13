import requests
import sys
import pandas as pd

headers = {
    "Authorization": "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"
}
story_points = 1
prompt = ''
AcceptanceCriteriaSubHeading = "Acceptance Crietria :"
model = "text-davinci-003"

# chatgpt input query

initial = "provide me jira story content only with sub-headings Summary , Description, Acceptance_Criteria, story points for "

# Authorization

api_key_chatgpt = "Chat_GPT-Key"
api_key = "Jira-Key"

# reading excel sheet

dataframe1 = pd.read_excel('story.xlsx')
topic_list = dataframe1['Topics'].tolist()

# method to get chatgpt response


def chat_with_chatgpt(prompt):
    res = requests.post(f"https://api.openai.com/v1/completions",
                        headers={
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {api_key_chatgpt}"
                        },
                        json={
                            "model": model,
                            "prompt": f"{prompt}",
                            "max_tokens": 4000,
                        }).json()
    return res['choices'][0]['text']


# method to create jira story

def jira_story(title, desc, storyPoints):
    res = requests.post(f"https://ukg10.atlassian.net/rest/api/2/issue/",
                        headers={
                            "Content-Type": "application/json",
                            "Authorization": f"Basic {api_key}"
                        },
                        json={

                            "expand": "renderedFields,names,schema,operations,editmeta,changelog,versionedRepresentations,customfield_10010 requestTypePractice",
                            "id": "10000",
                            "self": "https://ukg10.atlassian.net/rest/api/2/issue/10000",
                            "key": "UKG-1",
                            "fields": {
                                "issuetype":
                                {
                                    "self": "https://ukg10.atlassian.net/rest/api/2/issuetype/10001",
                                    "id": "10001",
                                    "description": "",
                                    "iconUrl": "https://ukg10.atlassian.net/rest/api/2/universal_avatar/view/type/issuetype/avatar/10315?size=medium", "name": "Story",
                                    "subtask": "false",
                                    "avatarId": 10315,
                                    "entityId": "0f6cfdb1-da4e-4151-8892-5c7212041160",
                                    "hierarchyLevel": 0
                                },
                                "project":
                                {
                                    "self": "https://ukg10.atlassian.net/rest/api/2/project/10000",
                                    "id": "10000",
                                    "key": "UKG",
                                    "name": "Ukg",
                                    "projectTypeKey": "software",
                                    "simplified": "true",
                                    "avatarUrls":
                                    {
                                        "48x48": "https://ukg10.atlassian.net/rest/api/2/universal_avatar/view/type/project/avatar/10424",
                                        "24x24": "https://ukg10.atlassian.net/rest/api/2/universal_avatar/view/type/project/avatar/10424?size=small",
                                        "16x16": "https://ukg10.atlassian.net/rest/api/2/universal_avatar/view/type/project/avatar/10424?size=xsmall",
                                        "32x32": "https://ukg10.atlassian.net/rest/api/2/universal_avatar/view/type/project/avatar/10424?size=medium"
                                    }
                                },
                                "labels": [],
                                "customfield_10021": [],
                                "customfield_10016": int(storyPoints),
                                "description": f"{desc}",
                                "summary": f"{title}"
                            }
                        }).json()
    return res

# iterating over excel sheet


for topic in topic_list:
    prompt = "".join([initial, topic])
    response = chat_with_chatgpt(prompt)
    with open("story.txt", "w") as f:
        f.write(f"{response}\n")
    file1 = open("story.txt", "r+")
    summary = file1.read()

    # parsing chatgpt response

    if (summary.count(":") == 4):
        summary = summary.split(":")
        title = summary[1].replace('\n', "").split('Description')[0]
        desc = summary[2].replace('\n', "").split('Acceptance')[
            0] + '\n' + AcceptanceCriteriaSubHeading + '\n' + summary[3].split('Story')[0]
        points_list = summary[4].replace('\n', "").split(' ')
        for point in points_list:
            if (point.isdigit()):
                story_points = int(point)
                break
        response1 = jira_story(title, desc, story_points)
    elif (summary.count(":") == 0):
        story_array = summary.split("Acceptance Criteria")
        title_and_description = story_array[0].replace(
            '\n', "").split('Description')
        title = title_and_description[0].split('Summary')[1]
        acceptance_criteria = story_array[1].split('Story Points')[0]
        storyPoints = story_array[1].split('Story Points')[1]
        desc = title_and_description[1] + '\n' + \
            "Acceptance Crietria :" + '\n' + acceptance_criteria
        points_list = storyPoints.replace('\n', "").split(' ')
        for point in points_list:
            if (point.isdigit()):
                story_points = int(point)
                break
        response1 = jira_story(title, desc, story_points)
