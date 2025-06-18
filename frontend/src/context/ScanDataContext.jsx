import React, { createContext, useContext, useState } from "react";

const ScanDataContext = createContext();

export const ScanDataProvider = ({ children }) => {
    const [reconData, setReconData] = useState(null);
    const [sqlScanResult, setSQLScanResult] = useState(null);
    const [xssScanResult, setXSSScanResult] = useState(null);

    return (
        <ScanDataContext.Provider value={{
            reconData,
            sqlScanResult,
            xssScanResult,
            setReconData,
            setSQLScanResult,
            setXSSScanResult
        }}>
            {children}
        </ScanDataContext.Provider>
    );
};

export const useScanData = () => useContext(ScanDataContext);
