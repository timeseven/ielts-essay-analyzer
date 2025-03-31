'use client';

import { motion } from 'motion/react';

const testimonials = [
	{
		quote: "StreamLine has revolutionized how our team collaborates. It's a game-changer!",
		author: 'Jane Doe',
		company: 'Tech Innovators Inc.',
	},
	{
		quote: 'The intuitive interface and powerful features make project management a breeze.',
		author: 'John Smith',
		company: 'Creative Solutions LLC',
	},
	{
		quote: "We've seen a 30% increase in productivity since adopting StreamLine.",
		author: 'Emily Johnson',
		company: 'Global Enterprises',
	},
];

export default function Testimonials() {
	return (
		<section id='testimonials' className='w-full bg-gray-50 py-12 md:py-24 lg:py-32'>
			<div className='container mx-auto px-4 md:px-6'>
				<motion.h2
					className='mb-12 text-center text-3xl font-bold'
					initial={{ opacity: 0, y: 20 }}
					animate={{ opacity: 1, y: 0 }}
					transition={{ duration: 0.5 }}
				>
					What Our Customers Say
				</motion.h2>
				<div className='grid grid-cols-1 gap-8 md:grid-cols-3'>
					{testimonials.map((testimonial, index) => (
						<motion.div
							key={index}
							className='rounded-lg bg-white p-6 shadow-md'
							initial={{ opacity: 0, y: 20 }}
							animate={{ opacity: 1, y: 0 }}
							transition={{ duration: 0.5, delay: index * 0.1 }}
						>
							<p className='mb-4 text-gray-600'>&quot;{testimonial.quote}&quot;</p>
							<p className='font-semibold'>{testimonial.author}</p>
							<p className='text-sm text-gray-500'>{testimonial.company}</p>
						</motion.div>
					))}
				</div>
			</div>
		</section>
	);
}
