import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY as string });

export interface ThreatAnalysis {
  threatLevel: number; // 0-100
  analysis: string;
  recommendation: string;
  isConfirmed: boolean;
}

export async function analyzeThreat(logData: string): Promise<ThreatAnalysis> {
  try {
    const response = await ai.models.generateContent({
      model: "gemini-3-flash-preview",
      contents: `Analyze the following MDB system logs for suspicious activity or unauthorized SuperBit access patterns. 
      Return a JSON analysis with threatLevel (0-100), analysis (brief explanation), recommendation, and isConfirmed (boolean).
      Logs: ${logData}`,
      config: {
        responseMimeType: "application/json",
      },
    });

    const result = JSON.parse(response.text || '{}');
    return {
      threatLevel: result.threatLevel ?? 0,
      analysis: result.analysis ?? "No anomalies detected in dimensional space.",
      recommendation: result.recommendation ?? "Maintain standard MDB monitoring.",
      isConfirmed: result.isConfirmed ?? false,
    };
  } catch (error) {
    console.error("Threat analysis failed:", error);
    return {
      threatLevel: 0,
      analysis: "Security Agent failed to sync with cloud threat intelligence.",
      recommendation: "Check network connection to MDB nodes.",
      isConfirmed: false,
    };
  }
}
