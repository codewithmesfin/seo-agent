import { render, screen } from '@testing-library/react';
import SEOGauge from '../components/charts/SEOGauge';

// Mock Recharts since it doesn't work well in JSDOM
jest.mock('recharts', () => ({
  ResponsiveContainer: ({ children }: any) => <div>{children}</div>,
  PieChart: ({ children }: any) => <div>{children}</div>,
  Pie: ({ children }: any) => <div>{children}</div>,
  Cell: () => <div />,
}));

describe('SEOGauge', () => {
  it('renders the label and score', () => {
    render(<SEOGauge score={85} label="Overall Score" />);
    expect(screen.getByText('Overall Score')).toBeDefined();
    expect(screen.getByText('85')).toBeDefined();
  });
});
