import { useEffect, useState } from "react";
import axios from "axios";

export default function RestockRecommendations() {
  const [recommendations, setRecommendations] = useState([]);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/restock/recommendations")
      .then((res) => {
        setRecommendations(res.data);
      })
      .catch((err) => {
        console.error(err);
      });
  }, []);

  return (
    <div
      style={{
        background: "#1e293b",
        color: "white",
        padding: "20px",
        borderRadius: "12px",
        marginTop: "30px",
      }}
    >
      <h2>📦 Smart Restock Recommendations</h2>

      {recommendations.map((item, index) => (
        <div
          key={index}
          style={{
            padding: "10px",
            borderBottom: "1px solid #334155",
          }}
        >
          <strong>{item.product}</strong>
          <br />
          Stock: {item.stock}
          <br />
          Recommendation: {item.recommendation}
        </div>
      ))}
    </div>
  );
}