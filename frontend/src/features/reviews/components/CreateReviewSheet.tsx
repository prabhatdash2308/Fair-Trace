import * as React from 'react';
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetDescription, SheetFooter } from '@/components/ui/sheet';
import { PrimaryButton } from '@/components/ui/PrimaryButton';
import { SecondaryButton } from '@/components/ui/SecondaryButton';
import { useEmployees } from '@/features/employees/hooks/useEmployees';
import { ReviewerAvatar } from '@/components/review';
import { Input } from '@/components/ui/input';

export interface CreateReviewSheetProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSubmit: (data: any) => void;
}

export const CreateReviewSheet: React.FC<CreateReviewSheetProps> = ({ open, onOpenChange, onSubmit }) => {
  const [step, setStep] = React.useState(1);
  const { data: employeesData, isLoading } = useEmployees();
  const [selectedEmployeeId, setSelectedEmployeeId] = React.useState<string>('');
  const [title, setTitle] = React.useState('');
  const [startDate, setStartDate] = React.useState('');
  const [endDate, setEndDate] = React.useState('');

  // Reset state on open change
  React.useEffect(() => {
    if (open) {
      setStep(1);
      setSelectedEmployeeId('');
      setTitle('');
      setStartDate('');
      setEndDate('');
    }
  }, [open]);

  const handleNext = () => setStep((s) => s + 1);
  const handleBack = () => setStep((s) => s - 1);

  const handleSubmit = () => {
    onSubmit({
      employee_id: selectedEmployeeId,
      title,
      review_period_start: startDate,
      review_period_end: endDate
    });
    onOpenChange(false);
  };

  const selectedEmployee = React.useMemo(() => 
    employeesData?.items.find(e => e.id === selectedEmployeeId) || null
  , [employeesData, selectedEmployeeId]);

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent side="right" className="sm:max-w-md w-full flex flex-col h-full bg-card">
        <SheetHeader>
          <SheetTitle>Create Review Cycle</SheetTitle>
          <SheetDescription>
            Step {step} of 4: {['Select Employee', 'Review Information', 'Objectives', 'Confirmation'][step - 1]}
          </SheetDescription>
        </SheetHeader>

        <div className="flex-1 overflow-y-auto py-6">
          {step === 1 && (
            <div className="space-y-4 fade-in">
              <h3 className="text-sm font-semibold tracking-tight">Select Employee</h3>
              {isLoading ? (
                <div className="text-sm text-muted-foreground">Loading employees...</div>
              ) : (
                <div className="flex flex-col gap-2">
                  {employeesData?.items.map(emp => (
                    <div 
                      key={emp.id}
                      onClick={() => setSelectedEmployeeId(emp.id)}
                      className={`flex items-center gap-3 p-3 rounded-md cursor-pointer border transition-colors ${
                        selectedEmployeeId === emp.id 
                          ? 'border-primary bg-primary/10' 
                          : 'border-border/50 hover:bg-muted/50'
                      }`}
                    >
                      <ReviewerAvatar employee={emp} />
                      <div className="flex flex-col">
                        <span className="text-sm font-medium">{emp.full_name}</span>
                        <span className="text-xs text-muted-foreground">{emp.role}</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {step === 2 && (
            <div className="space-y-4 fade-in">
              <h3 className="text-sm font-semibold tracking-tight">Review Information</h3>
              <div className="space-y-2">
                <label className="text-xs font-medium text-muted-foreground">Review Title</label>
                <Input 
                  placeholder="e.g. Q3 Performance Review" 
                  value={title} 
                  onChange={e => setTitle(e.target.value)} 
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="text-xs font-medium text-muted-foreground">Start Date</label>
                  <Input type="date" value={startDate} onChange={e => setStartDate(e.target.value)} />
                </div>
                <div className="space-y-2">
                  <label className="text-xs font-medium text-muted-foreground">End Date</label>
                  <Input type="date" value={endDate} onChange={e => setEndDate(e.target.value)} />
                </div>
              </div>
            </div>
          )}

          {step === 3 && (
            <div className="space-y-4 fade-in">
              <h3 className="text-sm font-semibold tracking-tight">Objectives & Criteria</h3>
              <p className="text-sm text-muted-foreground">
                Define the core objectives for this review cycle. 
                AI analysis will measure performance against these specific goals.
              </p>
              {/* Optional: Add dynamic objective inputs. For now it's static informational step. */}
              <div className="p-4 rounded-md border border-border/50 bg-muted/20 text-sm">
                Default Enterprise evaluation criteria will be applied.
              </div>
            </div>
          )}

          {step === 4 && (
            <div className="space-y-4 fade-in">
              <h3 className="text-sm font-semibold tracking-tight">Confirm Details</h3>
              <div className="p-4 rounded-md border border-border/50 bg-muted/20 space-y-3 text-sm">
                <div className="flex justify-between border-b border-border/50 pb-2">
                  <span className="text-muted-foreground">Employee</span>
                  <span className="font-medium">{selectedEmployee?.full_name}</span>
                </div>
                <div className="flex justify-between border-b border-border/50 pb-2">
                  <span className="text-muted-foreground">Title</span>
                  <span className="font-medium">{title}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Period</span>
                  <span className="font-medium">{startDate} to {endDate}</span>
                </div>
              </div>
              <p className="text-xs text-muted-foreground text-center">
                Clicking create will generate the cycle and transition it to the DRAFT stage.
              </p>
            </div>
          )}
        </div>

        <SheetFooter className="flex flex-row justify-between sm:justify-between pt-4 border-t border-border/50">
          <SecondaryButton onClick={step === 1 ? () => onOpenChange(false) : handleBack}>
            {step === 1 ? 'Cancel' : 'Back'}
          </SecondaryButton>
          <PrimaryButton 
            onClick={step === 4 ? handleSubmit : handleNext}
            disabled={
              (step === 1 && !selectedEmployeeId) || 
              (step === 2 && (!title || !startDate || !endDate))
            }
          >
            {step === 4 ? 'Create Review' : 'Next'}
          </PrimaryButton>
        </SheetFooter>
      </SheetContent>
    </Sheet>
  );
};
