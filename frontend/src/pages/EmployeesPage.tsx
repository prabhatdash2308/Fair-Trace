import * as React from 'react';
import { motion } from 'framer-motion';
import { pageTransition } from '@/components/motion';
import { PageSection } from '@/components/layout';
import { useEmployees } from '@/features/employees/hooks/useEmployees';
import {
  EmployeeHeader,
  EmployeeToolbar,
  EmployeeTable,
  EmployeeLoading
} from '@/features/employees/components';

export default function EmployeesPage() {
  const [searchValue, setSearchValue] = React.useState('');
  
  // Real backend query for employees
  const { data, isLoading } = useEmployees({ skip: 0, limit: 100 });

  // Client-side filter for now
  const filteredData = React.useMemo(() => {
    if (!data?.items) return [];
    if (!searchValue) return data.items;
    const lower = searchValue.toLowerCase();
    return data.items.filter(
      (e) => e.full_name.toLowerCase().includes(lower) || e.email.toLowerCase().includes(lower)
    );
  }, [data, searchValue]);

  return (
    <motion.div
      variants={pageTransition}
      initial="hidden"
      animate="visible"
      exit="exit"
      className="flex flex-col pb-12"
    >
      <EmployeeHeader />

      <PageSection>
        {isLoading ? (
          <EmployeeLoading />
        ) : (
          <div className="flex flex-col gap-4">
            <EmployeeToolbar 
              searchValue={searchValue}
              onSearchChange={setSearchValue}
            />
            <EmployeeTable 
              data={filteredData}
              isLoading={false}
            />
          </div>
        )}
      </PageSection>
    </motion.div>
  );
}
