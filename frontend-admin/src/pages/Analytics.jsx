import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js"
import { Bar } from "react-chartjs-2"

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
)

function Analytics() {
  const data = {
    labels: ["Mon", "Tue", "Wed", "Thu", "Fri"],
    datasets: [
      {
        label: "SOS Requests",
        data: [12, 19, 8, 15, 22],
        backgroundColor: "#6F4E37",
      },
    ],
  }

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">Analytics</h2>

      <div className="bg-white p-6 rounded-xl shadow">
        <Bar data={data} />
      </div>
    </div>
  )
}

export default Analytics