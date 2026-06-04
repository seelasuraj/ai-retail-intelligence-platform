import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";
import Charts from "./components/Charts";
import { motion } from "framer-motion";
import RestockRecommendations from "./components/RestockRecommendations";

export default function App() {
const [summary, setSummary] = useState(null);
const [topProducts, setTopProducts] = useState([]);
const [lowStock, setLowStock] = useState([]);
const [revenueData, setRevenueData] = useState([]);
const [insights, setInsights] = useState([]);
const [searchTerm, setSearchTerm] = useState("");
const [file, setFile] = useState(null);

  const fetchData = () => {
    axios
  .get("http://127.0.0.1:8000/analytics/insights")
  .then((res) => setInsights(res.data))
  .catch((err) => console.log(err));
    axios
  .get("http://127.0.0.1:8000/analytics/top-revenue")
  .then((res) => setRevenueData(res.data))
  .catch((err) => console.log(err));
    axios
      .get("http://127.0.0.1:8000/analytics/summary")
      .then((res) => setSummary(res.data))
      .catch((err) => console.log(err));

    axios
      .get("http://127.0.0.1:8000/analytics/top-products")
      .then((res) => setTopProducts(res.data))
      .catch((err) => console.log(err));

    axios
      .get("http://127.0.0.1:8000/analytics/low-stock")
      .then((res) => setLowStock(res.data))
      .catch((err) => console.log(err));
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleUpload = async () => {
    if (!file) {
      alert("Select file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      await axios.post(
        "http://127.0.0.1:8000/upload/",
        formData
      );

      alert("Upload Success");
      fetchData();
    } catch (err) {
      console.log(err);
      alert("Upload Failed");
    }
  };

  return (
    <div className="dashboard">
      {/* Sidebar */}
      <div className="sidebar">
        <h2>Retail AI</h2>
        <p> Dashboard</p>
        <p> Analytics</p>
        <p> Products</p>
      </div>

      {/* Main Content */}
      <div className="main-content">
        <h1 className="title">
          AI Retail Intelligence Platform
        </h1>
      <button
  onClick={() =>
    window.open(
      "http://127.0.0.1:8000/report/pdf",
      "_blank"
    )
  }
  style={{
    padding: "10px 20px",
    borderRadius: "8px",
    border: "none",
    cursor: "pointer",
    marginBottom: "20px",
    fontWeight: "bold",
  }}
>
  📄 Download PDF Report
</button>

        <div className="upload-box">
          <input
            type="file"
            accept=".csv"
            onChange={(e) =>
              setFile(e.target.files[0])
            }
          />
          <button onClick={handleUpload}>
            Upload CSV
          </button>
        </div>

        {/* Summary Cards */}
        {summary && (
          <div className="cards">
            <AnimatedCard
              title="Total Records"
              value={summary.total_records}
            />

            <AnimatedCard
              title="Total Stock"
              value={summary.total_stock}
            />

            <AnimatedCard
              title="Average Price"
              value={summary.average_price}
              prefix="₹"
            />

            <AnimatedCard
              title="Inventory Value"
              value={summary.inventory_value}
              prefix="₹"
            />
          </div>
        )}
        {/* Search Bar */}
<div className="search-container">
  <input
    type="text"
    placeholder=" Search products..."
    value={searchTerm}
    onChange={(e) => setSearchTerm(e.target.value)}
    className="search-input"
  />
</div>
        {/* Top Products */}
        <div className="table-container">
          <h2> Top Products</h2>

          <table>
            <thead>
              <tr>
                <th>Product</th>
                <th>Price</th>
              </tr>
            </thead>

            <tbody>
              {topProducts
              .filter((product) =>
    product.name
      .toLowerCase()
      .includes(searchTerm.toLowerCase())
  )
              .map((product, index) => (
                <tr key={index}>
                  <td>{product.name}</td>
                  <td>₹{product.price}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Low Stock Alerts */}
        <div className="table-container">
          <h2 className="warning-title">
             Low Stock Alerts
          </h2>

          <table>
            <thead>
              <tr>
                <th>Product</th>
                <th>Stock</th>
              </tr>
            </thead>

            <tbody>
              {lowStock.map((item, index) => (
                <tr key={index}>
                  <td>{item.name}</td>
                  <td>{item.stock}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
<div className="insights-container">
  <h2> AI Insights</h2>

  {insights.map((insight, index) => (
    <div key={index} className="insight-card">
      {insight}
    </div>
  ))}
</div>
        <Charts />
        <RestockRecommendations />

      </div>
    </div>
  );
}

function AnimatedCard({
  title,
  value,
  prefix = "",
}) {
  return (
    <motion.div
      className="card"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="card-label">{title}</div>

      <motion.div
        className="card-value"
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{
          type: "spring",
          stiffness: 100,
        }}
      >
        {prefix}
        {value}
      </motion.div>
    </motion.div>
  );
}