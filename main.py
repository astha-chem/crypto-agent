from src.agents.supervisor_agent import app, user_profiles, question_template
from src.utils.reporting_utils import create_report, print_messages
import uuid

def demo_report_by_investor_type(investor_type, user_question=None):
    print(f"Generating report for investor type: {investor_type}")
    investor_profile = user_profiles[investor_type]
    if user_question is None: 
        user_question = "How should I approach crypto investing now?"

    random_id = uuid.uuid4()
    config = {"configurable": {"thread_id": random_id}}
    result = app.invoke({
        "messages": [
            {
                "role": "user",
                "content": question_template.format(investor_profile=investor_profile, question=user_question)
            }
        ]
    }, 
    config)


    report_init = create_report(investor_profile, user_question=user_question, messages=result["messages"])

    with open(f"reports/report_{investor_type}.md", 'w', encoding='utf-8') as f:
        f.write(report_init)
    
    num_messages = print_messages(result["messages"])
    print(f"Report for {investor_type} saved to reports/report_{investor_type}.md")


def demo_multi_turn_conversation(investor_type="aggresive_young"):
    print(f"Starting multi-turn conversation for investor type: {investor_type}")
    questions = [
        "Crypto market seems to be falling. Should I buy more? ",
        "Thanks for your analysis. But I just lost my job. Should I still proceed with your recommendation? ", 
        "I still want to invest. How long should I wait? "
        ]
    investor_profile = user_profiles[investor_type]
    random_id = uuid.uuid4()
    config = {"configurable": {"thread_id": random_id}}
    result = app.invoke({
        "messages": [
            {
                "role": "user",
                "content": question_template.format(investor_profile=investor_profile, question=questions[0])
            }
        ]
    }, 
    config)

    num_messages = print_messages(result["messages"])

    print_messages(result["messages"])
    print("------------------------------")
    for question in questions[1:]:
        print("Next invocation with follow-up question: {question}")
        result = app.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": question
                },  
            ]
        }, config)

        new_messages = result["messages"][num_messages:]
        num_new_messages = print_messages(new_messages)
        num_messages += num_new_messages
        print("------------------------------")
    return result    


if __name__ == "__main__":
    demo_report_by_investor_type("recovery_investor")
    demo_report_by_investor_type("aggressive_young", user_question="Crypto market seems to be falling. Should I buy more? ")
    result = demo_multi_turn_conversation("aggressive_young")
    with open(f"reports/multi_turn_demo.md", "w", encoding='utf-8') as f:
        for msg in result["messages"]:
            f.write(msg.pretty_repr() + "\n---\n")