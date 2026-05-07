// Home Page - Hero section with quick recommendation form

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Hero Section */}
      <div className="relative overflow-hidden bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="relative z-10 pb-8 pt-16 sm:pb-12 sm:pt-24 lg:pt-32">
            <div className="mx-auto max-w-2xl text-center">
              <h1 className="text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl lg:text-6xl">
                Find Your Perfect{' '}
                <span className="text-primary-600">Restaurant</span>
              </h1>
              <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-gray-600">
                AI-powered restaurant recommendations tailored to your preferences. 
                Discover amazing dining experiences in your area.
              </p>
              
              {/* Quick Recommendation Form */}
              <div className="mt-10 sm:mt-12">
                <div className="bg-white p-8 rounded-lg shadow-lg border border-gray-200">
                  <form className="space-y-6">
                    <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
                      <div className="sm:col-span-2 lg:col-span-1">
                        <label htmlFor="location" className="block text-sm font-medium text-gray-700">
                          Location
                        </label>
                        <input
                          type="text"
                          id="location"
                          name="location"
                          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                          placeholder="e.g., Bellandur, Indiranagar"
                        />
                      </div>
                      
                      <div>
                        <label htmlFor="budget" className="block text-sm font-medium text-gray-700">
                          Budget Range
                        </label>
                        <div className="mt-1 grid grid-cols-2 gap-2">
                          <input
                            type="number"
                            id="minBudget"
                            name="minBudget"
                            className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                            placeholder="Min"
                          />
                          <input
                            type="number"
                            id="maxBudget"
                            name="maxBudget"
                            className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                            placeholder="Max"
                          />
                        </div>
                      </div>
                      
                      <div>
                        <label htmlFor="rating" className="block text-sm font-medium text-gray-700">
                          Minimum Rating
                        </label>
                        <select
                          id="rating"
                          name="rating"
                          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                        >
                          <option value="">Any Rating</option>
                          <option value="4.0">4.0+</option>
                          <option value="4.5">4.5+</option>
                          <option value="4.8">4.8+</option>
                        </select>
                      </div>
                      
                      <div className="sm:col-span-2 lg:col-span-1">
                        <label htmlFor="cuisines" className="block text-sm font-medium text-gray-700">
                          Preferred Cuisines
                        </label>
                        <input
                          type="text"
                          id="cuisines"
                          name="cuisines"
                          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                          placeholder="e.g., North Indian, Chinese, Italian"
                        />
                      </div>
                    </div>
                    
                    <div className="flex justify-center">
                      <button
                        type="submit"
                        className="inline-flex items-center justify-center rounded-md border border-transparent bg-primary-600 px-6 py-3 text-base font-medium text-white shadow-sm hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-colors"
                      >
                        Get Recommendations
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-12 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mt-12">
            <div className="text-center">
              <h2 className="text-3xl font-extrabold tracking-tight text-gray-900 sm:text-4xl">
                Why Choose Our AI Recommendations?
              </h2>
              <p className="mx-auto mt-4 max-w-2xl text-xl text-gray-600">
                Our intelligent system analyzes thousands of restaurants to find the perfect match for your preferences.
              </p>
            </div>
            
            <div className="mt-10">
              <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
                <div className="pt-6">
                  <div className="flow-root rounded-lg bg-gray-50 px-6 pb-8">
                    <div className="-mt-6">
                      <div>
                        <span className="inline-flex items-center justify-center rounded-md bg-primary-500 p-3 shadow-lg">
                          <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a2 2 0 002-2h-4a2 2 0 00-2 2m6 2a2 2 0 002-2h-4a2 2 0 00-2 2" />
                          </svg>
                        </span>
                      </div>
                      <h3 className="mt-8 text-lg font-medium tracking-tight text-gray-900">
                        AI-Powered
                      </h3>
                      <p className="mt-5 text-base text-gray-600">
                        Advanced machine learning algorithms analyze your preferences and provide personalized recommendations.
                      </p>
                    </div>
                  </div>
                </div>

                <div className="pt-6">
                  <div className="flow-root rounded-lg bg-gray-50 px-6 pb-8">
                    <div className="-mt-6">
                      <div>
                        <span className="inline-flex items-center justify-center rounded-md bg-primary-500 p-3 shadow-lg">
                          <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0m-9 10a9 9 0 01-9-9v4m0 0h18" />
                          </svg>
                        </span>
                      </div>
                      <h3 className="mt-8 text-lg font-medium tracking-tight text-gray-900">
                        Real-time Data
                      </h3>
                      <p className="mt-5 text-base text-gray-600">
                        Up-to-date restaurant information including ratings, prices, and availability.
                      </p>
                    </div>
                  </div>
                </div>

                <div className="pt-6">
                  <div className="flow-root rounded-lg bg-gray-50 px-6 pb-8">
                    <div className="-mt-6">
                      <div>
                        <span className="inline-flex items-center justify-center rounded-md bg-primary-500 p-3 shadow-lg">
                          <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M21 3h-2l-.4 2M7 13l-4 8h10.4" />
                          </svg>
                        </span>
                      </div>
                      <h3 className="mt-8 text-lg font-medium tracking-tight text-gray-900">
                        Quality Assured
                      </h3>
                      <p className="mt-5 text-base text-gray-600">
                        Comprehensive filtering ensures you get restaurants that match your exact preferences.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-primary-600">
        <div className="px-4 py-12 sm:px-6 sm:py-16 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
              Ready to Discover Amazing Restaurants?
            </h2>
            <p className="mx-auto mt-4 max-w-2xl text-xl text-primary-100">
              Get personalized recommendations in seconds. Start your culinary journey today.
            </p>
            <div className="mt-8 flex justify-center">
              <div className="inline-flex rounded-md shadow">
                <a
                  href="/recommendations"
                  className="inline-flex items-center justify-center rounded-md border border-transparent bg-white px-6 py-3 text-base font-medium text-primary-600 hover:bg-primary-50 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-colors"
                >
                  Get Started
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
