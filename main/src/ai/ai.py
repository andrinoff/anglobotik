from openai import OpenAI
import openai
import os

def check_essay(essay:str):
    client = OpenAI()
    openai.api_key = os.getenv('OPENAI_API_KEY')
    response = client.responses.create(
    model="gpt-4o",
    instructions="You are a russian teacher that checks essays for EGE and OGE in english, giving response in Russian.",
    input=f'оцени мне это эссе: "{essay}" по официальным критериям по эссе ЕГЭ и ОГЭ, давая оценку на каждый отдельный критерий',
)
    print(response.output_text)
    return response.output_text
    
def check_letter(letter:str):
    client = OpenAI()
    openai.api_key = os.getenv('OPENAI_API_KEY')
    response = client.responses.create(
    model="gpt-4o",
    instructions="You are a russian teacher that checks letters for EGE and OGE in english, giving response in Russian.",
    input=f'оцени мне это письмо: "{letter}" по официальным критериям письма ЕГЭ и ОГЭ, давая оценку на каждый отдельный критерий',
)
    print(response.output_text)
    return response.output_text
    
check_essay(essay = "Essay why some Zetlanders are not keen on theatre going Nowadays there are many ways how people can spend their free time, some of them go to the theatre or cinema, another part prefer stay at home with family. I have found the results of a survey about why some people do not like to go to the theatre. I am going to comment on several key findings from the data. As can be seen from the survey results, the most popular reason is “Too expensive” (52%), while the least popular reason is “ inconvenient time of performance” (6%). Compared to the data in the table, the theatre is too far from home is only 5% more than people have other interests (18% vs 13%). It is surprising that options “too expensive” and “online broadcasts available” have such a big gap in 41% (52% vs 11%) because watch some shows on the TV is more chipper than in a special places. As the result we can identify a problem, usually performances in the theatre are really long and the schedule of them is not comfortable for working people because the biggest part of shows available on weekdays. This issue can be addressed. Theatre administration has to change the time schedule of plays and make them shorter, maybe cut them by parts.  In conclusion, based on the findings above, I would say that personally I keen on going to theatre, I think for people who like reading it is a good experience and everyone should spend their weekend for a play.")