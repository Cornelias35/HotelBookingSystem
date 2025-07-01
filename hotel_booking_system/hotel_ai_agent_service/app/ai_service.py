from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode
from langgraph.graph import START, StateGraph
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.tools import tool
from fastapi import APIRouter
import httpx
from app.models import AIState, RoomType
from typing import Optional

router = APIRouter(prefix="/v1/ai_agent", tags=["AI Agent"])
@router.get("/ai-service")
def ai_agent(prompt : str, is_authenticated : bool, user_id : int):
    load_dotenv()

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    tools = [get_hotels, get_hotel_ratings, make_reservation]

    llm_with_tools = llm.bind_tools(tools)
    sys_msg = SystemMessage(
        content="You are helpful customer support agent that works on hotel management system."
            "Provide information to user when it is needed."
            "To answering question that user asked, use tools only, do not answer from your knowledge"
            f"This is user_id {user_id} and this is whether user is authenticated {is_authenticated}. Use them when needed."
            "If user tells like x city , y country, use x and y as , input to city and country parameters."
    )
    def assistant(state: AIState):
        return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}
    
    builder = StateGraph(AIState)

    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(tools))

    builder.add_edge(START, "assistant")
    builder.add_conditional_edges(
        "assistant",
        tools_condition,
    )
    builder.add_edge("tools", "assistant")
    react_graph = builder.compile()

    messages = [HumanMessage(content=prompt)]
    response = react_graph.invoke({"messages" : messages})

    for m in response["messages"]:
        m.pretty_print()

    return {"ai_message": response["messages"][-1].content}

        


@tool
def get_hotels(
    city: str, 
    country: str, 
    start_date: str, 
    end_date: str, 
    number_of_rooms: int,
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
    url = "http://127.0.0.1:8000/v1/hotels/get_hotels"
    params={
        "city": city, 
        "country": country,
        "start_date":start_date,
        "end_date":end_date,
        "number_of_rooms":number_of_rooms,
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
    url = f"http://127.0.0.1:8003/api/v1/comments/{hotel_id}/comment_stats"
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

    url = "http://127.0.0.1:8001/v1/book_service/book_room"
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