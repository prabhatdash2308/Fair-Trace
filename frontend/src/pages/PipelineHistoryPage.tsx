import * as React from 'react';
import { motion } from 'framer-motion';
import { pageTransition } from '@/components/motion';
import { PipelineEmpty } from '@/features/pipeline/components/PipelineEmpty';

export default function PipelineHistoryPage() {
  // Empty state until backend historical pipeline endpoint is implemented
  return (
    <motion.div
      variants={pageTransition}
      initial="hidden"
      animate="visible"
      exit="exit"
      className="flex flex-col items-center justify-center h-[80vh]"
    >
      <PipelineEmpty />
    </motion.div>
  );
}
