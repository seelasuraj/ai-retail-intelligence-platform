import { useEffect, useState } from "react";
import axios from "axios";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  PieChart,
  Pie,
  Cell,
  Legend,
  LineChart,
  Line,
} from "recharts";

const COLORS = ["#8884d8", "#82ca9d", "#ffc658", "#ff8042", "#0088fe"];

export default function Charts() {
  const [data, setData] = useState([]);
const [revenueData, setRevenueData] = useState([]);
const [forecast, setForecast] = useState(null);
const [selectedProduct, setSelectedProduct] = useState("");
const [products, setProducts] = useState([]);
  // Load analytics (once)
useEffect(() => {
  axios
    .get("http://127.0.0.1:8000/analytics/top-products")
    .then((res) => {
      setData(res.data || []);
      setProducts(res.data || []);
    })
    .catch((err) => {
      console.log(err);
      setData([]);
      setProducts([]);
    });

  axios
    .get("http://127.0.0.1:8000/analytics/top-revenue")
    .then((res) => setRevenueData(res.data || []))
    .catch((err) => {
      console.log(err);
      setRevenueData([]);
    });
}, []);

useEffect(() => {
  if (products.length > 0 && !selectedProduct) {
    setSelectedProduct(products[0].name);
  }
}, [products, selectedProduct]);
  // Load forecast whenever product changes
  useEffect(() => {
  if (!selectedProduct) return;

  axios
    .get(
      `http://127.0.0.1:8000/forecast/forecast/${selectedProduct}`
    )
    .then((res) => {
      console.log("FORECAST DATA:", res.data);
      setForecast(res.data);
    })
    .catch((err) => {
      console.log("Forecast API error:", err);
      setForecast(null);
    });
}, [selectedProduct]);
  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        gap: "40px",
        flexWrap: "wrap",
        marginTop: "40px",
        padding: "20px",
      }}
    >
      {/* 📊 PRODUCT PRICE CHART */}
      <div
        style={{
          padding: "20px",
          borderRadius: "12px",
          boxShadow: "0 4px 12px rgba(0,0,0,0.2)",
          background: "#1e293b",
          color: "white",
        }}
      >
        <h3 style={{ textAlign: "center" }}> Product Price Overview</h3>

        <BarChart width={400} height={300} data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="price" fill="#8884d8" />
        </BarChart>
      </div>

      {/* 🥧 PIE CHART */}
      <div
        style={{
          padding: "20px",
          borderRadius: "12px",
          boxShadow: "0 4px 12px rgba(0,0,0,0.2)",
          background: "#1e293b",
          color: "white",
        }}
      >
        <h3 style={{ textAlign: "center" }}> Price Distribution</h3>

        <PieChart width={400} height={300}>
          <Pie
            data={data}
            dataKey="price"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={100}
            label
          >
            {data.map((_, index) => (
              <Cell
                key={index}
                fill={COLORS[index % COLORS.length]}
              />
            ))}
          </Pie>

          <Tooltip />
          <Legend />
        </PieChart>
      </div>

      {/* 💰 REVENUE CHART */}
      <div
        style={{
          padding: "20px",
          borderRadius: "12px",
          boxShadow: "0 4px 12px rgba(0,0,0,0.2)",
          background: "#1e293b",
          color: "white",
        }}
      >
        <h3 style={{ textAlign: "center" }}> Revenue Analytics</h3>

        <BarChart width={500} height={300} data={revenueData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="revenue" fill="#22c55e" />
        </BarChart>
      </div>

      {/* 🤖 AI FORECAST SECTION */}
      <div style={{ width: "100%" }}>
        {/* PRODUCT SELECTOR */}
        <div style={{ textAlign: "center", marginBottom: "20px" }}>
          <label style={{ color: "white", marginRight: "10px" }}>
            Select Product:
          </label>

          <select
  value={selectedProduct}
  onChange={(e) => setSelectedProduct(e.target.value)}
>
  {products.map((product, index) => (
    <option
      key={index}
      value={product.name}
    >
      {product.name}
    </option>
  ))}
</select>
        </div>

        {/* FORECAST DISPLAY */}
        {forecast && (
<div
  style={{
    padding: "20px",
    borderRadius: "12px",
    boxShadow: "0 4px 12px rgba(0,0,0,0.2)",
    background: "#0f172a",
    color: "white",
    maxWidth: "900px",
    margin: "0 auto",
  }}
>
    <h2 style={{ textAlign: "center" }}>
       AI Demand Forecast
    </h2>

    <div style={{ textAlign: "center", marginBottom: "10px" }}>
       Product: <b>{forecast.product}</b>
    </div>

    <div style={{ textAlign: "center", marginBottom: "15px" }}>
       Next Predicted Demand:{" "}
      <b style={{ color: "#22c55e" }}>
        {forecast.predicted_next}
      </b>
    </div>

    {forecast.sales_history &&
    forecast.sales_history.length > 0 ? (
      <>
        <LineChart
          width={700}
          height={300}
          data={[
            ...(forecast.sales_history || []).map((val, i) => ({
              day: i + 1,
              sales: val,
            })),
            {
              day:
                (forecast.sales_history || []).length + 1,
              sales: forecast.predicted_next,
            },
          ]}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="day" />
          <YAxis />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="sales"
            stroke="#f97316"
            strokeWidth={3}
          />
        </LineChart>

        <div
          style={{
            textAlign: "center",
            marginTop: "10px",
            fontSize: "12px",
            color: "#94a3b8",
          }}
        >
           Powered by Linear Regression Model
        </div>
      </>
    ) : (
      <div
        style={{
          textAlign: "center",
          padding: "30px",
          fontSize: "18px",
          color: "#f97316",
          fontWeight: "bold",
        }}
      >
         No sales history available for this product
      </div>
    )}
  </div>
)}
      </div>
    </div>
  );
}