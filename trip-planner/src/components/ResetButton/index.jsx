'use client';
import { useState } from 'react';
import {Button} from "@mui/material";
import styles from "./ResetButton.module.css";
import TripForm from "../TripForm";

function ResetButton() {
    const handleReset = () => {
        window.location.reload();
    };
    return (
        <Button
            onClick={handleReset}
            variant="contained"
            color="secondary"
            className={styles.resetButton}
        >
            Reset the search
        </Button>
    );
}
export default ResetButton;