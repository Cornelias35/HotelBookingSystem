import React, { useState, useEffect } from "react";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  useNavigate,
  useParams,
} from "react-router-dom";
import "./App.css";

const BASE_URL = "http://localhost:8000";

const SERVICE_URLS = {
  search: "/search_service/v1/search/get_hotels",
  hotelDetails: "/admin_service/v1/hotels/get_hotel_id",
  comments: "/comments_service/api/v1/comments",
  commentStats: "/comments_service/api/v1/comments",
  book: "/book_service/v1/book_service/book_room",
  ai: "/ai_agent_service/v1/ai_agent/ai-service",
};

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/hotel/:hotelId" element={<HotelDetail />} />
      </Routes>
    </Router>
  );
}

function MainPage() {
  const [city, setCity] = useState("");
  const [country, setCountry] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [numberOfPeople, setNumberOfPeople] = useState(1);
  const [hotels, setHotels] = useState([]);
  const navigate = useNavigate();

  const searchHotels = async () => {
    const params = new URLSearchParams({
      city,
      country,
      start_date: startDate,
      end_date: endDate,
      number_of_people: numberOfPeople.toString(),
    });
    const res = await fetch(`${SERVICE_URLS.search}?${params}`);
    const data = await res.json();
    setHotels(data);
  };

  return (
    <div className="container">
      <h1>Hotel Booking System</h1>
      <div className="form-row">
        <input
          type="date"
          placeholder="Start Date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
        />
        <input
          type="date"
          placeholder="End Date"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
        />
        <input
          type="text"
          placeholder="City"
          value={city}
          onChange={(e) => setCity(e.target.value)}
        />
        <input
          type="text"
          placeholder="Country"
          value={country}
          onChange={(e) => setCountry(e.target.value)}
        />
        <input
          type="number"
          placeholder="People"
          value={numberOfPeople}
          onChange={(e) => setNumberOfPeople(parseInt(e.target.value))}
        />
        <button onClick={searchHotels}>Search</button>
      </div>
      <ul className="hotel-list">
        {hotels.map((hotel: any) => (
          <li key={hotel.id} onClick={() => navigate(`/hotel/${hotel.id}`)}>
            {hotel.name} - {hotel.city}, {hotel.country}
          </li>
        ))}
      </ul>
      <ChatWidget />
    </div>
  );
}

function HotelDetail() {
  const { hotelId } = useParams();
  const [hotel, setHotel] = useState<any>(null);
  const [comments, setComments] = useState([]);
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    const fetchDetails = async () => {
      const res = await fetch(
        `${BASE_URL}${SERVICE_URLS.hotelDetails}?hotel_id=${hotelId}`
      );
      const data = await res.json();
      setHotel(data);

      const statsRes = await fetch(
        `${BASE_URL}${SERVICE_URLS.commentStats}/${hotelId}/comment_stats`
      );
      setStats(await statsRes.json());

      const commentsRes = await fetch(
        `${BASE_URL}${SERVICE_URLS.comments}/${hotelId}`
      );
      setComments(await commentsRes.json());
    };
    fetchDetails();
  }, [hotelId]);

  const handleBooking = async () => {
    const res = await fetch(SERVICE_URLS.book, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        hotel_id: hotelId,
        room_type: "standard",
        start_date: "2025-07-15",
        end_date: "2025-07-20",
      }),
    });
    const data = await res.json();
    alert("Booking completed!" + JSON.stringify(data));
  };

  if (!hotel) return <div className="container">Loading...</div>;

  return (
    <div className="container">
      <h2>{hotel.name}</h2>
      <p>
        {hotel.city}, {hotel.country}
      </p>
      <p>Details to be filled later...</p>
      <h4>Comments Summary</h4>
      <p>Average Rating: {stats?.average_rating}</p>
      <ul className="comment-list">
        {comments.map((c: any, idx: number) => (
          <li key={idx}>{c.text}</li>
        ))}
      </ul>
      <button className="book-button" onClick={handleBooking}>
        Book Now
      </button>
      <ChatWidget />
    </div>
  );
}

function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState<string[]>([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    const res = await fetch(
      `${SERVICE_URLS.ai}?prompt=${encodeURIComponent(input)}`
    );
    const data = await res.json();
    setMessages([...messages, `You: ${input}`, `AI: ${data.response}`]);
    setInput("");
  };

  return (
    <div className="chat-widget">
      {open ? (
        <div className="chat-box">
          <div className="chat-header">Chat with AI</div>
          <div className="chat-body">
            {messages.map((msg, idx) => (
              <div key={idx}>{msg}</div>
            ))}
          </div>
          <div className="chat-footer">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />
            <button onClick={sendMessage}>Send</button>
            <button onClick={() => setOpen(false)}>Close</button>
          </div>
        </div>
      ) : (
        <button className="chat-button" onClick={() => setOpen(true)}>
          Chat
        </button>
      )}
    </div>
  );
}

export default App;
