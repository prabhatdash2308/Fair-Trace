import * as React from 'react';
import { motion } from 'framer-motion';
import { pageTransition } from '@/components/motion';
import { 
  ReviewHeader, 
  ReviewToolbar, 
  ReviewStatusTabs, 
  ReviewTable, 
  CreateReviewSheet 
} from '@/features/reviews/components';
import { useReviewCycles, useCreateCycle } from '@/features/reviews/hooks/useReviews';
import { useToast } from '@/components/ui/use-toast';

export default function ReviewsPage() {
  const [searchTerm, setSearchTerm] = React.useState('');
  const [activeStatus, setActiveStatus] = React.useState('ALL');
  const [isCreateSheetOpen, setIsCreateSheetOpen] = React.useState(false);
  const { toast } = useToast();

  const { data: cyclesData, isLoading, refetch } = useReviewCycles();
  const createCycle = useCreateCycle();

  const handleCreateSubmit = (data: any) => {
    createCycle.mutate(data, {
      onSuccess: () => {
        toast({
          title: "Review Created",
          description: "The new review cycle has been created successfully.",
          variant: "success",
        });
        refetch();
      },
      onError: (err: any) => {
        toast({
          title: "Error",
          description: err.message || "Failed to create review cycle.",
          variant: "destructive",
        });
      }
    });
  };

  const filteredData = React.useMemo(() => {
    if (!cyclesData?.items) return [];
    let filtered = cyclesData.items;

    if (activeStatus !== 'ALL') {
      filtered = filtered.filter(c => c.status === activeStatus);
    }

    if (searchTerm) {
      filtered = filtered.filter(c => 
        c.title.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    return filtered;
  }, [cyclesData, activeStatus, searchTerm]);

  return (
    <motion.div
      variants={pageTransition}
      initial="hidden"
      animate="visible"
      exit="exit"
      className="flex flex-col gap-2 pb-12 w-full max-w-7xl mx-auto"
    >
      <ReviewHeader onCreateClick={() => setIsCreateSheetOpen(true)} />
      
      <div className="bg-card border border-border/50 rounded-xl overflow-hidden shadow-sm">
        <div className="px-6 pt-2">
          <ReviewToolbar searchTerm={searchTerm} onSearchChange={setSearchTerm} />
          <ReviewStatusTabs activeStatus={activeStatus} onStatusChange={setActiveStatus} />
        </div>
        <ReviewTable data={filteredData} isLoading={isLoading} />
      </div>

      <CreateReviewSheet 
        open={isCreateSheetOpen} 
        onOpenChange={setIsCreateSheetOpen} 
        onSubmit={handleCreateSubmit} 
      />
    </motion.div>
  );
}
