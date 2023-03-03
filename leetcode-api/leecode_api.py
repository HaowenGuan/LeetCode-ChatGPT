#%% Activate API
from __future__ import annotations
import leetcode
from time import sleep

# Get the next two values from your browser cookies
leetcode_session = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMTQ4NTQ4MiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjZhNjBlMzhlYmY2MTViOWQ2NGIzZWY4MTA3NDQyMTc4YmRlYmYzODgiLCJpZCI6MTQ4NTQ4MiwiZW1haWwiOiI4NTEwMjM1NjFAcXEuY29tIiwidXNlcm5hbWUiOiJFWEJPUk4iLCJ1c2VyX3NsdWciOiJFWEJPUk4iLCJhdmF0YXIiOiJodHRwczovL2Fzc2V0cy5sZWV0Y29kZS5jb20vdXNlcnMvYXZhdGFycy9hdmF0YXJfMTY2NTExMjMwNS5wbmciLCJyZWZyZXNoZWRfYXQiOjE2Nzc3ODA4NTIsImlwIjoiNzEuMTcyLjQxLjQiLCJpZGVudGl0eSI6IjhmNmEyMzhlM2FkMzgyZGFiYzJhNTVmMTRiMGYxNGRjIiwiX3Nlc3Npb25fZXhwaXJ5IjoxMjA5NjAwLCJzZXNzaW9uX2lkIjozNDI2ODIxMn0.4_wCRUB4yNqSPFnukhGX6nCY0ybGgzu-H9Q2cKvNBvY"
csrf_token = "7oAfAKkxhGSWx7GzfGlXxjXCuudpRloqvQLTOz77K4lEYvO79ZFKlwqphAILP6qv"

# Experimental: Or CSRF token can be obtained automatically
import leetcode.auth

csrf_token = leetcode.auth.get_csrf_cookie(leetcode_session)

configuration = leetcode.Configuration()

configuration.api_key["x-csrftoken"] = csrf_token
configuration.api_key["csrftoken"] = csrf_token
configuration.api_key["LEETCODE_SESSION"] = leetcode_session
configuration.api_key["Referer"] = "https://leetcode.com"
configuration.debug = False
print('wtf')
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
    print("Question ----------------------------")
    soup = BeautifulSoup(output.data.question.content, "html.parser")
    # print(" ".join(soup.get_text(separator=" ").split()))
    print(soup.get_text())
    print("Initial Code ------------------------")
    print(output.data.question.code_snippets[2].code)
    if hasattr(output.data.question, "hint"):
        print('Hint')
        print(output.data.question.hint)
    print("stats -------------------------------")
    print(output.data.question.stats)

    return api_response

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
output = get_problem(problem="Longest-Substring-Without-Repeating-Characters")
# %%
