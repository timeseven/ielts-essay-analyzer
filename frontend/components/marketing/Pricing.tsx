import { Check } from 'lucide-react';
import { Button } from '@/components/ui/button';

const plans = [
	{
		name: 'Basic',
		price: '$9.99',
		features: ['Up to 5 team members', 'Basic task management', '1GB storage', 'Email support'],
	},
	{
		name: 'Pro',
		price: '$24.99',
		features: ['Up to 20 team members', 'Advanced task management', '10GB storage', 'Priority support'],
	},
	{
		name: 'Enterprise',
		price: 'Custom',
		features: ['Unlimited team members', 'Custom features', 'Unlimited storage', 'Dedicated support'],
	},
];

export default function Pricing() {
	return (
		<section id='pricing' className='w-full bg-white py-12 md:py-24 lg:py-32'>
			<div className='container mx-auto px-4 md:px-6'>
				<h2 className='mb-12 text-center text-3xl font-bold'>Choose Your Plan</h2>
				<div className='grid grid-cols-1 gap-8 md:grid-cols-3'>
					{plans.map((plan, index) => (
						<div key={index} className='rounded-lg border p-6 shadow-md'>
							<h3 className='mb-2 text-xl font-semibold'>{plan.name}</h3>
							<p className='mb-4 text-3xl font-bold'>{plan.price}</p>
							<ul className='mb-6'>
								{plan.features.map((feature, featureIndex) => (
									<li key={featureIndex} className='mb-2 flex items-center'>
										<Check className='mr-2 h-5 w-5 text-green-500' />
										<span>{feature}</span>
									</li>
								))}
							</ul>
							<Button className='w-full'>Choose Plan</Button>
						</div>
					))}
				</div>
			</div>
		</section>
	);
}
