'use client';

import { CheckCircle, Zap, Users, TrendingUp } from 'lucide-react';
import { motion } from 'motion/react';

const features = [
	{
		icon: CheckCircle,
		title: 'Task Management',
		description: 'Easily create, assign, and track tasks across your team.',
	},
	{
		icon: Zap,
		title: 'Real-time Collaboration',
		description: 'Work together seamlessly with live updates and in-app messaging.',
	},
	{
		icon: Users,
		title: 'Team Analytics',
		description: "Gain insights into your team's performance and productivity.",
	},
	{
		icon: TrendingUp,
		title: 'Progress Tracking',
		description: 'Visualize project progress with interactive charts and reports.',
	},
];

export default function Features() {
	return (
		<section id='features' className='w-full bg-white py-12 md:py-24 lg:py-32'>
			<div className='container mx-auto px-4 md:px-6'>
				<motion.h2
					className='mb-12 text-center text-3xl font-bold'
					initial={{ opacity: 0, y: 20 }}
					animate={{ opacity: 1, y: 0 }}
					transition={{ duration: 0.5 }}
				>
					Powerful Features
				</motion.h2>
				<div className='grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-4'>
					{features.map((feature, index) => (
						<motion.div
							key={index}
							className='flex flex-col items-center text-center'
							initial={{ opacity: 0, y: 20 }}
							animate={{ opacity: 1, y: 0 }}
							transition={{ duration: 0.5, delay: index * 0.1 }}
						>
							<feature.icon className='mb-4 h-12 w-12 text-blue-600' />
							<h3 className='mb-2 text-xl font-semibold'>{feature.title}</h3>
							<p className='text-gray-600'>{feature.description}</p>
						</motion.div>
					))}
				</div>
			</div>
		</section>
	);
}
