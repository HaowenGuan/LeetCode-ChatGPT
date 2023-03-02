from __future__ import annotations
import leetcode
# Get the next two values from your browser cookies
leetcode_session = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMTQ4NTQ4MiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjZhNjBlMzhlYmY2MTViOWQ2NGIzZWY4MTA3NDQyMTc4YmRlYmYzODgiLCJpZCI6MTQ4NTQ4MiwiZW1haWwiOiI4NTEwMjM1NjFAcXEuY29tIiwidXNlcm5hbWUiOiJFWEJPUk4iLCJ1c2VyX3NsdWciOiJFWEJPUk4iLCJhdmF0YXIiOiJodHRwczovL2Fzc2V0cy5sZWV0Y29kZS5jb20vdXNlcnMvYXZhdGFycy9hdmF0YXJfMTY2NTExMjMwNS5wbmciLCJyZWZyZXNoZWRfYXQiOjE2Nzc1OTY4ODAsImlwIjoiMjE2LjE2NS45NS4xNjUiLCJpZGVudGl0eSI6IjhmNmEyMzhlM2FkMzgyZGFiYzJhNTVmMTRiMGYxNGRjIiwiX3Nlc3Npb25fZXhwaXJ5IjoxMjA5NjAwLCJzZXNzaW9uX2lkIjozNDI2ODIxMn0.Fv0a_Cq87EWmph4RKjzc22kTOMVMoz-jXYRq7XT4mZ4"
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

api_instance = leetcode.DefaultApi(leetcode.ApiClient(configuration))
#%% First Step Status Checking
def status_check():
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
#%% Developing
from time import sleep

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
                companyTagStats
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
    variables=leetcode.GraphqlQueryGetQuestionDetailVariables(title_slug="two-sum"),
    operation_name="getQuestionDetail",
)

# print(api_instance.graphql_post(body=graphql_request))

# Get stats
api_response = api_instance.api_problems_topic_get(topic="shell")

print("Stats of this session")
# print(api_response)
print('skip stats')

#%% Only Test given test case
code = """
class Solution:
    def twoSum(self, nums, target):
        record = {}
        for i, n in enumerate(nums):
            if target - n in record.keys():
                return [record[target - n], i]
            record[n] = i
"""

test_submission = leetcode.TestSubmission(
    data_input="[2,7,11,15]\n9",
    typed_code=code,
    question_id=1,
    test_mode=False,
    lang="python",
)

interpretation_id = api_instance.problems_problem_interpret_solution_post(
    problem="two-sum", body=test_submission
)

print("Test has been queued. Result:")
print(interpretation_id)

sleep(5)  # FIXME: should probably be a busy-waiting loop

test_submission_result = api_instance.submissions_detail_id_check_get(
    id=interpretation_id.interpret_id
)

#%% Real submission to leetcode, submission with be record!
code = """
class Solution:
    def twoSum(self, nums, target):
        record = {}
        for i, n in enumerate(nums):
            if target - n in record.keys():
                return [record[target - n], i]
            record[n] = i
"""

test_submission = leetcode.Submission(
    judge_type="large",
    typed_code=code,
    question_id=1,
    test_mode=False,
    lang="python",
)

interpretation_id = api_instance.problems_problem_submit_post(
    problem="two-sum", body=test_submission
)

print("Test has been queued. Result:")
print(interpretation_id)

sleep(5)  # FIXME: should probably be a busy-waiting loop

test_submission_result = api_instance.submissions_detail_id_check_get(
    id=interpretation_id.interpret_id
)
#%%
# print("Got test result:")
# print(leetcode.TestSubmissionResult(**test_submission_result))
#%%
# def test1():


#     print("Got test result:")
#     print(leetcode.TestSubmissionResult(**test_submission_result))

#     # Real submission
#     submission = leetcode.Submission(
#         judge_type="large", typed_code=code, question_id=1, test_mode=False, lang="python"
#     )

#     submission_id = api_instance.problems_problem_submit_post(
#         problem="two-sum", body=submission
#     )

#     print("Submission has been queued. Result:")
#     print(submission_id)

#     sleep(5)  # FIXME: should probably be a busy-waiting loop

#     submission_result = api_instance.submissions_detail_id_check_get(
#         id=submission_id.submission_id
#     )

#     print("Got submission result:")
#     print(leetcode.SubmissionResult(**submission_result))



# if __name__ == '__main__':
#     status_check()
#     test1()

