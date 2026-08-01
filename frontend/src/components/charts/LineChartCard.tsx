import * as React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { ChartContainer, type ChartContainerProps } from './ChartContainer';

export interface LineChartCardProps extends ChartContainerProps {
  data: any[];
  xAxisKey: string;
  seriesKeys: { key: string; color?: string; name?: string }[];
}

export const LineChartCard: React.FC<LineChartCardProps> = ({
  data,
  xAxisKey,
  seriesKeys,
  isLoading,
  isEmpty,
  ...props
}) => {
  const isActuallyEmpty = isEmpty || !data || data.length === 0;

  return (
    <ChartContainer isLoading={isLoading} isEmpty={isActuallyEmpty} {...props}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--border)" opacity={0.5} />
          <XAxis 
            dataKey={xAxisKey} 
            axisLine={false} 
            tickLine={false} 
            tick={{ fontSize: 12, fill: 'var(--muted-foreground)' }} 
            dy={10} 
          />
          <YAxis 
            axisLine={false} 
            tickLine={false} 
            tick={{ fontSize: 12, fill: 'var(--muted-foreground)' }} 
          />
          <Tooltip
            contentStyle={{ 
              backgroundColor: 'var(--background)', 
              borderRadius: '8px',
              border: '1px solid var(--border)',
              boxShadow: '0 4px 20px -4px rgba(0,0,0,0.1)'
            }}
            itemStyle={{ fontSize: 13, fontWeight: 500 }}
            labelStyle={{ fontSize: 12, color: 'var(--muted-foreground)', marginBottom: '4px' }}
          />
          {seriesKeys.map((s, idx) => (
            <Line
              key={s.key}
              type="monotone"
              dataKey={s.key}
              name={s.name || s.key}
              stroke={s.color || 'hsl(var(--foreground))'}
              strokeWidth={2}
              dot={{ r: 3, fill: 'var(--background)', strokeWidth: 2 }}
              activeDot={{ r: 5 }}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </ChartContainer>
  );
};
