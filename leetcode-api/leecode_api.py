#%% Activate API
from __future__ import annotations
import leetcode
from time import sleep

# Get the next two values from your browser cookies
leetcode_session = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzb2NpYWxhY2NvdW50X3NvY2lhbGxvZ2luIjp7ImFjY291bnQiOnsiaWQiOm51bGwsInVzZXJfaWQiOm51bGwsInByb3ZpZGVyIjoiZ29vZ2xlIiwidWlkIjoiMTE2MjE5OTc3NDg5ODgzMzQ2Njk3IiwibGFzdF9sb2dpbiI6bnVsbCwiZGF0ZV9qb2luZWQiOm51bGwsImV4dHJhX2RhdGEiOnsiaWQiOiIxMTYyMTk5Nzc0ODk4ODMzNDY2OTciLCJlbWFpbCI6ImhsamJhenhAZ21haWwuY29tIiwidmVyaWZpZWRfZW1haWwiOnRydWUsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9kZWZhdWx0LXVzZXI9czk2LWMifX0sInVzZXIiOnsiaWQiOm51bGwsInBhc3N3b3JkIjoiIUlYdERHcTJaNVk0OTdpWno2M1I2WGEwRGdFVzNvTnBuQ3Q3SWhUQXoiLCJsYXN0X2xvZ2luIjpudWxsLCJpc19zdXBlcnVzZXIiOmZhbHNlLCJ1c2VybmFtZSI6IiIsImZpcnN0X25hbWUiOiIiLCJsYXN0X25hbWUiOiIiLCJlbWFpbCI6ImhsamJhenhAZ21haWwuY29tIiwiaXNfc3RhZmYiOmZhbHNlLCJpc19hY3RpdmUiOnRydWUsImRhdGVfam9pbmVkIjoiMjAyMy0wMy0wMlQwMDo0ODoxNC4yMDBaIn0sInN0YXRlIjp7Im5leHQiOiIvIiwicHJvY2VzcyI6ImxvZ2luIiwic2NvcGUiOiIiLCJhdXRoX3BhcmFtcyI6IiJ9LCJlbWFpbF9hZGRyZXNzZXMiOlt7ImlkIjpudWxsLCJ1c2VyX2lkIjpudWxsLCJlbWFpbCI6ImhsamJhenhAZ21haWwuY29tIiwidmVyaWZpZWQiOnRydWUsInByaW1hcnkiOnRydWV9XSwidG9rZW4iOnsiaWQiOm51bGwsImFwcF9pZCI6MSwiYWNjb3VudF9pZCI6bnVsbCwidG9rZW4iOiJ5YTI5LmEwQVZ2WlZzcGdiQzdKQ05HZmpDTkg4emV5MVpuNU92alVGRWIxUFlVNnJKSUJpYXgwZHBQRXFoZVFYX3Job092bkYxV1kzSlF4OUItTXozemFCTm5TZWhxYmNkRmxKNUFKM2taWjU5bThOdi1OQkFXMmlYTlBoeFIzcmxLQk9XbU1pZ05mWmJhNVNBMmtTbmZ0R2IzcC1QYlpZZFVwYUNnWUtBVnNTQVJJU0ZRR2Jkd2FJdE1RVTE3b2ZJdWtCYldNcWR5Q1MtZzAxNjMiLCJ0b2tlbl9zZWNyZXQiOiIiLCJleHBpcmVzX2F0IjoiMjAyMy0wMy0wMlQwMTo0ODoxMy4wNTVaIn19LCJfYXV0aF91c2VyX2lkIjoiNDg2MzA0NyIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImJkYjk0OWVhZjI3YjcyOTExZDNlODkzYjc1NWE3NmQ0MWE4ZmQ5MDYiLCJpZCI6NDg2MzA0NywiZW1haWwiOiJobGpiYXp4QGdtYWlsLmNvbSIsInVzZXJuYW1lIjoiU2VsZW5hX3p4IiwidXNlcl9zbHVnIjoiU2VsZW5hX3p4IiwiYXZhdGFyIjoiaHR0cHM6Ly9zMy11cy13ZXN0LTEuYW1hem9uYXdzLmNvbS9zMy1sYy11cGxvYWQvYXNzZXRzL2RlZmF1bHRfYXZhdGFyLmpwZyIsInJlZnJlc2hlZF9hdCI6MTY3NzcxODE2MywiaXAiOiIxMDAuOC4yMjIuMjAxIiwiaWRlbnRpdHkiOiIwOGM4NmFmOWQxZTUxZWFiZGUzY2EyMGM1ZTI5MzMwOCIsInNlc3Npb25faWQiOjM1OTc5MTg3LCJfc2Vzc2lvbl9leHBpcnkiOjEyMDk2MDB9.GEkJH5VpXcLiOUxV1_vbjj2uCMc5-RlIa1vosOluPGI;"
csrf_token = "LRiEmCdcNLbMowaKQE1pAwDXQO6jUf53l9x2OfjWQaSod2EdBKjHjrQbTFrT6q"

# Experimental: Or CSRF token can be obtained automatically
import leetcode.auth

csrf_token = leetcode.auth.get_csrf_cookie(leetcode_session)

configuration = leetcode.Configuration()

configuration.api_key["x-csrftoken"] = csrf_token
configuration.api_key["csrftoken"] = csrf_token
configuration.api_key["LEETCODE_SESSION"] = leetcode_session
configuration.api_key["Referer"] = "https://leetcode.com"
configuration.debug = False

api_instance = leetcode.DefaultApi(leetcode.ApiClient(configuration))


#%% Status Checking
def status_check():
    """
    Check leetcode API status
    :return:
    """
    graphql_request = leetcode.GraphqlQuery(
        query="""
    {
        user {
        username
        isCurrentUserPremium
        }
    }
    """,
        variables=leetcode.GraphqlQueryVariables(),
    )
    print(api_instance.graphql_post(body=graphql_request))


status_check()
# %% Developing
# from time import sleep
#
# graphql_request = leetcode.GraphqlQuery(
#     query="""
#             query getQuestionDetail($titleSlug: String!) {
#             question(titleSlug: $titleSlug) {
#                 questionId
#                 questionFrontendId
#                 boundTopicId
#                 title
#                 content
#                 translatedTitle
#                 isPaidOnly
#                 difficulty
#                 likes
#                 dislikes
#                 isLiked
#                 similarQuestions
#                 contributors {
#                 username
#                 profileUrl
#                 avatarUrl
#                 __typename
#                 }
#                 langToValidPlayground
#                 topicTags {
#                 name
#                 slug
#                 translatedName
#                 __typename
#                 }
#                 companyTagStats
#                 codeSnippets {
#                 lang
#                 langSlug
#                 code
#                 __typename
#                 }
#                 stats
#                 codeDefinition
#                 hints
#                 solution {
#                 id
#                 canSeeDetail
#                 __typename
#                 }
#                 status
#                 sampleTestCase
#                 enableRunCode
#                 metaData
#                 translatedContent
#                 judgerAvailable
#                 judgeType
#                 mysqlSchemas
#                 enableTestMode
#                 envInfo
#                 __typename
#             }
#             }
#         """,
#     variables=leetcode.GraphqlQueryGetQuestionDetailVariables(title_slug="two-sum"),
#     operation_name="getQuestionDetail",
# )
#
# # print(api_instance.graphql_post(body=graphql_request))
#
# # Get stats
# api_response = api_instance.api_problems_topic_get(topic="shell")
#
# print("Stats of this session")
# # print(api_response)
# print('skip stats')


# %% Only Test given test case
def test_submission(id: int, code: str, test_case: str, lang="python"):
    """
    Test submission, will not be recorded
    :param id: question id
    :param code: code
    :param lang: code language
    :return: status
    """
    test_data = leetcode.TestSubmission(
        data_input=test_case,
        typed_code=code,
        question_id=id,
        test_mode=False,
        lang=lang,
    )

    interpretation_id = api_instance.problems_problem_interpret_solution_post(
        problem="two-sum", body=test_data
    )

    print("Test has been queued. Result:")
    print(interpretation_id)

    sleep(5)  # FIXME: should probably be a busy-waiting loop

    test_submission_result = api_instance.submissions_detail_id_check_get(
        id=interpretation_id.interpret_id
    )
    return test_submission_result


#%% Real submission to LeetCode, submission with be record
def submission(id: int, code: str, lang="python"):
    """
    Real submission, will be recorded to leetcode account
    :param id: question id
    :param code: code
    :param lang: code language
    :return: status
    """
    submission = leetcode.Submission(
        judge_type="large",
        typed_code=code,
        question_id=id,
        test_mode=False,
        lang=lang,
    )

    interpretation_id = api_instance.problems_problem_submit_post(
        problem="two-sum", body=submission
    )

    print("Test has been queued. Result:")
    print(interpretation_id)

    sleep(5)  # FIXME: should probably be a busy-waiting loop

    submission_result = api_instance.submissions_detail_id_check_get(
        id=interpretation_id.submission_id
    )
    return submission_result

#%% Get Question Detail
def get_problem_list(problem="algorithms"):
    """
    Real submission, will be recorded to leetcode account
    :param id: question id
    :param code: code
    :param lang: code language
    :return: status
    """
    # query = leetcode.GraphqlQueryGetQuestionDetailVariables(title_slug=problem)
    api_response = api_instance.api_problems_topic_get(topic=problem)
    print("Get Question Result:")
    print(api_response)

    return api_response
output = get_problem_list()

#%% Get Question Detail
from bs4 import BeautifulSoup
def get_problem(problem="two-sum"):
    graphql_request = leetcode.GraphqlQuery(
        query="""
                query getQuestionDetail($titleSlug: String!) {
                question(titleSlug: $titleSlug) {
                    questionId
                    questionFrontendId
                    boundTopicId
                    title
                    content
                    translatedTitle
                    isPaidOnly
                    difficulty
                    likes
                    dislikes
                    isLiked
                    similarQuestions
                    contributors {
                    username
                    profileUrl
                    avatarUrl
                    __typename
                    }
                    langToValidPlayground
                    topicTags {
                    name
                    slug
                    translatedName
                    __typename
                    }
                    codeSnippets {
                    lang
                    langSlug
                    code
                    __typename
                    }
                    stats
                    codeDefinition
                    hints
                    solution {
                    id
                    canSeeDetail
                    __typename
                    }
                    status
                    sampleTestCase
                    enableRunCode
                    metaData
                    translatedContent
                    judgerAvailable
                    judgeType
                    mysqlSchemas
                    enableTestMode
                    envInfo
                    __typename
                }
                }
            """,
        variables=leetcode.GraphqlQueryGetQuestionDetailVariables(title_slug=problem),
        operation_name="getQuestionDetail",
    )

    api_response = api_instance.graphql_post(body=graphql_request)
    # print("Question ----------------------------")
    
    # soup = BeautifulSoup(api_response.data.question.content, "html.parser")
    # # print(" ".join(soup.get_text(separator=" ").split()))
    # print(soup.get_text())
    # print("Initial Code ------------------------")
    # print(api_response.data.question.code_snippets[2].code)
    # if hasattr(api_response.data.question, "hint"):
    #     print('Hint')
    #     print(api_response.data.question.hint)
    # print("stats -------------------------------")
    # print(api_response.data.question.stats)
    
    question_str = "Question ----------------------------\n"
    
    soup = BeautifulSoup(api_response.data.question.content, "html.parser")
    print(str(soup))
    question_str += soup.get_text()
    question_str += "\nInitial Code ------------------------\n"
    question_str += api_response.data.question.code_snippets[2].code
    if hasattr(api_response.data.question, "hint"):
        question_str += '\nHint\n'
        question_str += api_response.data.question.hint

    print("stats -------------------------------")
    print(api_response.data.question.stats)

    return str(soup)

# %%
code = """
class Solution:
    def twoSum(self, nums, target):
        record = {}
        for i, n in enumerate(nums):
            if target - n in record.keys():
                # return [1]
                return [record[target - n], i]
            record[n] = i
"""
test_case = "[2,7,11,15]\n9"
lang = "python"
status_check()
# %%
status = test_submission(1, code, test_case, lang="python")
print(status)
# %%
status = submission(1, code, lang="python")
print(status)

# %%
output = get_problem(problem="Minimum-Time-to-Visit-a-Cell-In-a-Grid")
# %%
import json
import openai
import os
openai.api_key = "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"

messages = [
    # system message first, it helps set the behavior of the assistant
    {"role": "system", "content": "Let's do some coding questions!"}]
message = "Write python codes to answer the following question:\n" + output
if message:
    messages.append(
        {"role": "user", "content": message},
    )
    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages
    )

reply = chat_completion.choices[0].message.content
print(f"🤖: {reply}")
messages.append({"role": "assistant", "content": reply})
# %%
