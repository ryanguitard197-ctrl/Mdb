import express from "express";
import { createServer as createViteServer } from "vite";
import path from "path";
import fs from "fs";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function startServer() {
  const app = express();
  const PORT = 3000;

  app.use(express.json());

  // Mock Remote Repository for MDB OS
  const remoteApps = [
    {
      id: "firefox",
      name: "Mozilla Firefox",
      description: "Fast, private and open source web browser.",
      version: "124.0.1",
      icon: "Globe",
      size: "72MB",
      category: "Classic"
    },
    {
      id: "vscode",
      name: "VS Code",
      description: "Code editing. Redefined.",
      version: "1.87.2",
      icon: "Code",
      size: "154MB",
      category: "Classic"
    },
    {
      id: "gimp",
      name: "GIMP",
      description: "GNU Image Manipulation Program.",
      version: "2.10.36",
      icon: "Image",
      size: "98MB",
      category: "Classic"
    },
    {
      id: "libreoffice",
      name: "LibreOffice",
      description: "The world's most popular open source office suite.",
      version: "7.6.5",
      icon: "FileText",
      size: "215MB",
      category: "Classic"
    },
    {
      id: "vlc",
      name: "VLC Player",
      description: "Simple, fast and powerful multimedia player.",
      version: "3.5.4",
      icon: "Music",
      size: "42MB",
      category: "Classic"
    },
    {
      id: "quantum-lab",
      name: "Quantum Research Suite",
      description: "Laboratory for SuperBit research and quantum simulations.",
      version: "1.0.0",
      icon: "Cpu",
      size: "12MB",
      category: "Experimental"
    }
  ];

  // API Routes
  app.get("/api/apps", (req, res) => {
    const { q } = req.query;
    if (q) {
      const filtered = remoteApps.filter(a => 
        a.name.toLowerCase().includes(String(q).toLowerCase()) || 
        a.description.toLowerCase().includes(String(q).toLowerCase())
      );
      return res.json(filtered);
    }
    res.json(remoteApps);
  });

  app.post("/api/apps/install", (req, res) => {
    const { appId } = req.body;
    const appData = remoteApps.find(a => a.id === appId);
    if (!appData) return res.status(404).json({ error: "App not found" });
    
    // Simulate installation logic
    console.log(`Installing ${appId}...`);
    res.json({ success: true, message: `${appData.name} installed successfully.` });
  });

  // Source Export API for Mobile Users
  app.get("/api/export-source", async (req, res) => {
    try {
      const mod = await import("jszip");
      const JSZipClass = (mod as any).default || mod;
      const zip = new JSZipClass();
      
      const filesToInclude = [
        "kernel/mdb_kernel.cpp",
        "kernel/mdb_core.c",
        "kernel/mdb_arch.h",
        "kernel/mdbfs.c",
        "kernel/Makefile",
        "scripts/make_iso.sh",
        "Cargo.toml",
        "main.rs",
        "BUILD_GUIDE.md",
        "server.ts",
        "src/App.tsx",
        "package.json"
      ];

      for (const file of filesToInclude) {
        try {
          const filePath = path.join(process.cwd(), file);
          if (fs.existsSync(filePath)) {
            const content = fs.readFileSync(filePath, 'utf8');
            zip.file(file, content);
          }
        } catch (e) {
          console.warn(`Could not include ${file} in export`, e);
        }
      }

      const content = await zip.generateAsync({ type: "nodebuffer" });
      res.setHeader('Content-Type', 'application/zip');
      res.setHeader('Content-Disposition', 'attachment; filename=mdb-os-source.zip');
      res.send(content);
    } catch (error) {
      console.error("Export Error:", error);
      res.status(500).json({ error: "Failed to create source zip" });
    }
  });

  // Vite middleware for development
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), "dist");
    app.use(express.static(distPath));
    app.get("*", (req, res) => {
      res.sendFile(path.join(distPath, "index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`MDB OS Server running on http://localhost:${PORT}`);
  });
}

startServer();
