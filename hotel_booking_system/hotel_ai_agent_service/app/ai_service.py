from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode
from langgraph.graph import START, StateGraph, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.tools import tool
from fastapi import APIRouter, Request
import httpx
from app.models import AIState, RoomType
from typing import Optional, Literal

router = APIRouter(tags=["AI Agent"])
@router.get("/ai-service")
def ai_agent(prompt : str, request: Request, chat_summary : str = ""): #
    load_dotenv()

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    user_id_str = None
    if user_id_str is not None:
        try:
            user_id = int(user_id_str)

        except ValueError:
            user_id = -1  
    else:
        user_id = -1

    is_authenticated = request.headers.get("X-Is-Authenticated", "false").lower() == "true"

    print(f"User ID: {user_id}, Is Authenticated: {is_authenticated}")

    tools = [get_hotels, get_hotel_ratings, make_reservation]

    llm_with_tools = llm.bind_tools(tools)
    sys_msg = SystemMessage(
        content="You are helpful customer support agent that works on hotel management system."
            "Provide information to user when it is needed."
            "To answering question that user asked, use tools only, do not answer from your knowledge"
            f"This is user_id {user_id} and this is whether user is authenticated {is_authenticated}. Use them when needed."
            "If user tells like x city , y country, use x and y as , input to city and country parameters."
            "If user_id is -1, it means that user is not logged in. Ask them to log in if they want to make reservation."
    )
    def assistant(state: AIState):
        return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

    def route_tools(state : AIState) -> Literal["tools", "summary_node"]:
        if isinstance(state, list):
            ai_message = state[-1]
        elif messages := state.get("messages", []):
            ai_message = messages[-1]
        else:
            raise ValueError(f"No messages found in input state to tool_edge: {state}")
        if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
            return "tools"
        return "summary_node"

    def summarize_conversation(state : AIState):
        if state["summary"]:
            summary_prev = state["summary"]
            summary_message = (
                f"Summary of previous conversation: {summary_prev}\n\n"
                "Update this summary with the new messages above. Include everything that is told."
            )
        else:
            summary_message = "Create a summary of the conversation above:"

        messages = state["messages"] + [HumanMessage(content=summary_message)]
        response = llm.invoke(messages)
        return {"summary": response.content, "messages": state["messages"]}

    builder = StateGraph(AIState)

    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(tools))
    builder.add_node("summary_node", summarize_conversation)

    builder.add_edge(START, "assistant")
    builder.add_conditional_edges("assistant", route_tools)
    builder.add_edge("tools", "assistant")
    builder.add_edge("summary_node", END)

    react_graph = builder.compile()

    initial_state = {
        "messages" : [HumanMessage(content=prompt)],
        "user_id": user_id,
        "is_authenticated": is_authenticated,
        "summary": chat_summary
    }
    response = react_graph.invoke(initial_state)


    return_value = {
        "ai_message": response["messages"][-1].content,
        "summary": response["summary"]
    }

    return return_value

        


@tool
def get_hotels(
    city: str, 
    country: str, 
    start_date: str, 
    end_date: str, 
    number_of_people: int,
):
    """
    This is the function to get available hotels between specified dates and city, country. Use it when user asks about hotels it asked.
    Args:
        city : str
        country : str
        start_date : str in "year-mm-dd" format
        end_date : str in "year-mm-dd" format
        number_of_rooms : int
    """
    url = "http://hotel-admin-service:8000/get_hotels"
    params={
        "city": city, 
        "country": country,
        "start_date":start_date,
        "end_date":end_date,
        "number_of_rooms":number_of_people,
    }

    response = httpx.get(url=url, params=params) 
    json_data = response.json()
    print(json_data)
    return json_data

@tool
def get_hotel_ratings(
    hotel_id:int
):
    """ 
    This function returns average ratings of hotel. Use it when user wants information about hotel.

    Args :
        hotel_id
    """
    url = f"http://hotel-comments-service:8000/{hotel_id}/comment_stats"
    params = {
        "hotel_id":hotel_id
    }
    response = httpx.get(url=url, params=params)
    json_data = response.json()
    return json_data

@tool
def make_reservation(
    user_id : int,
    user_name : str,
    hotel_id : int,
    number_of_people : int,
    room_type : RoomType,
    start_date : str,
    end_date : str,
    is_authenticated : bool
):
    """ 
    Use this function to make reservation as user asked. You should provide hotel_id, number_of_people, start_date, end_date from what user asked.

    Args:
        user_id : int
        user_name : str
        hotel_id : int
        number_of_people : int
        room_type : RoomType
        start_date : str
        end_date : str
        is_authenticated : bool
    """

    url = "http://book-hotel-service:8000/book_room"
    json = {
        "user_id" : user_id,
        "user_name" : user_name,
        "hotel_id" : hotel_id,
        "number_of_people":number_of_people,
        "room_type" : room_type,
        "start_date":start_date,
        "end_date":end_date,
        "is_authenticated":is_authenticated
    }
    response = httpx.post(url=url, json=json)
    json_data = response.json()
    return json_data
