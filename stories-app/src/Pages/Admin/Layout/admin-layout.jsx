// AdminLayout.tsx
import { SidebarProvider } from "../../../context/SidebarContext";
import { ThemeProvider } from "../../../context/ThemeContext";
import LayoutContent from "../../../layout/AppLayout"; // ou inclure directement AppSidebar + Header
import "./admin.css"
const AdminLayout = () => {
  return (
    <ThemeProvider>
        <SidebarProvider>
            <LayoutContent /> {/* AppSidebar + AppHeader + Outlet */}
        </SidebarProvider>
    </ThemeProvider>
    
  );
};

export default AdminLayout;
