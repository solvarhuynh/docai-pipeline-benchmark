import { useEffect, useState } from "react";
import { ContractPage } from "./pages/ContractPage";
import { HomePage } from "./pages/HomePage";
import { InvoicePage } from "./pages/InvoicePage";
import { ResearchPage } from "./pages/ResearchPage";

type Route = "/" | "/invoice" | "/contract" | "/research";

function currentRoute(): Route {
  const path = window.location.pathname as Route;
  return ["/", "/invoice", "/contract", "/research"].includes(path) ? path : "/";
}

export default function App() {
  const [route, setRoute] = useState<Route>(currentRoute);

  useEffect(() => {
    const handleNavigation = () => setRoute(currentRoute());
    window.addEventListener("popstate", handleNavigation);
    return () => window.removeEventListener("popstate", handleNavigation);
  }, []);

  const navigate = (nextRoute: Route) => {
    window.history.pushState({}, "", nextRoute);
    setRoute(nextRoute);
  };

  return (
    <div className="app-shell">
      <header className="topbar">
        <button className="brand" onClick={() => navigate("/")}>DocAI</button>
        <nav aria-label="Primary navigation">
          {([['/invoice', 'Invoice'], ['/contract', 'Contract'], ['/research', 'Research Lab']] as const).map(([path, label]) => (
            <button className={route === path ? "nav-link active" : "nav-link"} key={path} onClick={() => navigate(path)}>
              {label}
            </button>
          ))}
        </nav>
      </header>
      <main>
        {route === "/" && <HomePage />}
        {route === "/invoice" && <InvoicePage />}
        {route === "/contract" && <ContractPage />}
        {route === "/research" && <ResearchPage />}
      </main>
      <footer>React + TypeScript + Vite frontend · FastAPI backend</footer>
    </div>
  );
}
