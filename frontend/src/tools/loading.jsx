import React from "react";
import { motion } from "framer-motion";
import './../css/loader.css'

const loadingContainer = {
  width: "7rem",
  height: "3rem",
  display: "flex",
  justifyContent: "space-around"
};

const loadingCircle = {
  width: "1.5rem",
  height: "1.5rem",
  backgroundColor: "black",
  borderRadius: "0.75rem"
};

const loadingContainerVariants = {
  start: {
    transition: {
      staggerChildren: 0.2
    }
  },
  end: {
    transition: {
      staggerChildren: 0.2
    }
  }
};

const loadingCircleVariants = {
  start: {
    y: "50%"
  },
  end: {
    y: "150%"
  }
};

const loadingCircleTransition = {
  duration: 0.5,
  yoyo: Infinity,
  ease: "easeInOut"
};

export default function ThreeDotsWave() {
  return (
    <motion.div
      style={loadingContainer}
      variants={loadingContainerVariants}
      initial="start"
      animate="end"
      class="loader loaderContainer"
    >
      <motion.span
        style={loadingCircle}
        variants={loadingCircleVariants}
        transition={loadingCircleTransition}
        class="loader"
      />
      <motion.span
        style={loadingCircle}
        variants={loadingCircleVariants}
        transition={loadingCircleTransition}
        class="loader"
      />
      <motion.span
        style={loadingCircle}
        variants={loadingCircleVariants}
        transition={loadingCircleTransition}
        class="loader"
      />
    </motion.div>
  );
}