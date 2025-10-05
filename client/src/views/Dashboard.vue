<template>
  <div class="page-content">
    <div class="container-fluid">
      <!-- start page title -->
      <div class="row align-items-center">
        <div class="col-sm-6">
          <div class="page-title-box">
            <h4 class="font-size-18">Dashboard</h4>
            <ol class="breadcrumb mb-0">
              <li class="breadcrumb-item active">Welcome to Veltrix Dashboard</li>
            </ol>
          </div>
        </div>

        <div class="col-sm-6">
          <div class="float-end d-none d-md-block">
            <div class="dropdown">
              <button class="btn btn-primary dropdown-toggle waves-effect waves-light" 
                  type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                  <i class="mdi mdi-cog mr-2"></i> Settings
              </button>
              <div class="dropdown-menu dropdown-menu-right">
                <a class="dropdown-item" href="#">Action</a>
                <a class="dropdown-item" href="#">Another action</a>
                <a class="dropdown-item" href="#">Something else here</a>
                <div class="dropdown-divider"></div>
                <a class="dropdown-item" href="#">Separated link</a>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- end page title -->

      <!-- Stat Cards -->
        <div class="row">
          <div class="col-xl-3 col-md-6">
            <WidgetStat 
              title="Sales" 
              value="$12,890" 
              subText="+16.24%" 
              color="success" 
              image="@/assets/images/small/img-1.jpg"
            />
          </div>
          <div class="col-xl-3 col-md-6">
            <WidgetStat 
              title="New Users" 
              value="1,845" 
              subText="+2.50%" 
              color="primary" 
              image="@/assets/images/small/img-2.jpg"
            />
          </div>
          <div class="col-xl-3 col-md-6">
            <WidgetStat 
              title="Products" 
              value="145" 
              subText="-1.50%" 
              color="warning" 
              image="@/assets/images/small/img-3.jpg"
            />
          </div>
          <div class="col-xl-3 col-md-6">
            <WidgetStat 
              title="Comments" 
              value="2,541" 
              subText="+8.30%" 
              color="danger" 
              image="@/assets/images/small/img-4.jpg"
            />
          </div>
        </div>
      <!-- end row -->

      <!-- Monthly Earning Chart -->
      <div class="row">
        <div class="col-xl-8">
          <div class="card">
            <div class="card-body">
              <div class="float-right d-none d-md-block">
                <div class="btn-group mb-2">
                  <button type="button" class="btn btn-sm btn-light">
                    Monthly
                  </button>
                  <button type="button" class="btn btn-sm btn-light">
                    Yearly
                  </button>
                </div>
              </div>
              <h4 class="card-title mb-4">Monthly Earnings</h4>
              <div class="mb-4">
                <div class="row">
                  <div class="col-sm-6">
                    <p class="text-muted mb-2">Total Earnings</p>
                    <h3 class="font-weight-bold">$25,890</h3>
                  </div>
                  <div class="col-sm-6">
                    <p class="text-muted mb-2">Target</p>
                    <div class="mt-4">
                      <div class="w-100 h-2 bg-light rounded">
                        <div class="h-2 rounded bg-primary" style="width: 65%"></div>
                      </div>
                    </div>
                    <p class="text-muted mt-2">65% of target achieved</p>
                  </div>
                </div>
              </div>
              <div>
                    <WidgetChart/>
                  </div>
            </div>
          </div>
        </div>

        <!-- Sales Analytics -->
        <div class="col-xl-4">
          <div class="card">
            <div class="card-body">
              <h4 class="card-title mb-4">Sales Analytics</h4>
              <div class="mb-5">
                <div class="text-center">
                  <p class="text-muted mb-1">Total Revenue</p>
                  <h3 class="font-weight-bold">$26,500</h3>
                </div>
              </div>
              <div class="mb-4">
                <div class="row">
                  <div class="col-sm-6">
                    <p class="text-muted mb-1">Today</p>
                    <div class="d-flex align-items-center">
                      <h4 class="font-weight-bold mr-2">$1,800</h4>
                      <span class="text-success font-size-12"><i class="mdi mdi-arrow-up"></i> 2.5%</span>
                    </div>
                  </div>
                  <div class="col-sm-6">
                    <p class="text-muted mb-1">This Week</p>
                    <div class="d-flex align-items-center">
                      <h4 class="font-weight-bold mr-2">$6,250</h4>
                      <span class="text-danger font-size-12"><i class="mdi mdi-arrow-down"></i> 1.5%</span>
                    </div>
                  </div>
                </div>
              </div>
              <div>
                <div class="mb-4">
                  <div class="d-flex justify-content-between mb-2">
                    <span class="text-muted text-sm">Product A</span>
                    <span class="text-muted text-sm">75%</span>
                  </div>
                  <div class="w-100 h-2 bg-light rounded">
                    <div class="h-2 rounded bg-primary" style="width: 75%"></div>
                  </div>
                </div>
                <div class="mb-4">
                  <div class="d-flex justify-content-between mb-2">
                    <span class="text-muted text-sm">Product B</span>
                    <span class="text-muted text-sm">60%</span>
                  </div>
                  <div class="w-100 h-2 bg-light rounded">
                    <div class="h-2 rounded bg-success" style="width: 60%"></div>
                  </div>
                </div>
                <div class="mb-4">
                  <div class="d-flex justify-content-between mb-2">
                    <span class="text-muted text-sm">Product C</span>
                    <span class="text-muted text-sm">45%</span>
                  </div>
                  <div class="w-100 h-2 bg-light rounded">
                    <div class="h-2 rounded bg-info" style="width: 45%"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- end row -->

      <!-- Sales Report -->
      <div class="row">
        <div class="col-xl-4">
          <div class="card">
            <div class="card-body">
              <h4 class="card-title mb-4">Sales Report</h4>
              <div class="text-center mb-4">
                <div class="mb-3">
                  <div id="sales-pie-chart" class="mx-auto" style="height: 230px;"></div>
                </div>
                <div class="row">
                  <div class="col-4">
                    <div class="text-center">
                      <div class="font-weight-bold text-primary mb-1">$12,500</div>
                      <div class="text-muted text-sm">Product A</div>
                    </div>
                  </div>
                  <div class="col-4">
                    <div class="text-center">
                      <div class="font-weight-bold text-success mb-1">$9,500</div>
                      <div class="text-muted text-sm">Product B</div>
                    </div>
                  </div>
                  <div class="col-4">
                    <div class="text-center">
                      <div class="font-weight-bold text-info mb-1">$4,500</div>
                      <div class="text-muted text-sm">Product C</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Activity -->
        <div class="col-xl-4">
          <div class="card">
            <div class="card-body">
              <h4 class="card-title mb-4">Activity</h4>
              <WidgetActivity :activityData="activityData" />
            </div>
          </div>
        </div>

        <!-- Order Success Card -->
        <div class="col-xl-4">
          <div class="card">
            <div class="card-body">
              <div class="float-right">
                <button type="button" class="btn btn-outline-primary btn-sm">
                  View All
                </button>
              </div>
              <h4 class="card-title mb-4">Order Success</h4>
              <div class="text-center mb-5">
                <div class="inline-block position-relative">
                  <div class="inline-block font-size-36 text-primary font-weight-bold">95%</div>
                  <div class="inline-block text-muted text-sm ml-1">Success</div>
                </div>
              </div>
              <div class="mb-4">
                <div class="d-flex justify-content-between mb-2">
                  <span class="text-muted">Completed</span>
                  <span class="text-muted">190</span>
                </div>
                <div class="w-100 h-2 bg-light rounded">
                  <div class="h-2 rounded bg-primary" style="width: 95%"></div>
                </div>
              </div>
              <div class="mb-4">
                <div class="d-flex justify-content-between mb-2">
                  <span class="text-muted">Pending</span>
                  <span class="text-muted">5</span>
                </div>
                <div class="w-100 h-2 bg-light rounded">
                  <div class="h-2 rounded bg-warning" style="width: 3%"></div>
                </div>
              </div>
              <div>
                <div class="d-flex justify-content-between mb-2">
                  <span class="text-muted">Canceled</span>
                  <span class="text-muted">5</span>
                </div>
                <div class="w-100 h-2 bg-light rounded">
                  <div class="h-2 rounded bg-danger" style="width: 2%"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- end row -->

      <!-- Popular Products & Customer Reviews -->
      <div class="row">
        <div class="col-xl-4">
          <div class="card">
            <div class="card-body">
              <div class="float-right">
                <button type="button" class="btn btn-outline-primary btn-sm">
                  View All
                </button>
              </div>
              <h4 class="card-title mb-4">Popular Products</h4>
              <div class="table-responsive">
                <table class="table table-hover mb-0">
                  <thead>
                    <tr>
                      <th>Product</th>
                      <th>Sales</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="product in popularProducts" :key="product.id">
                      <td>
                        <div class="d-flex align-items-center">
                          <img :src="product.image" alt class="avatar-xs rounded-circle mr-2" />
                          {{ product.name }}
                        </div>
                      </td>
                      <td class="font-weight-medium">{{ product.sales }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <div class="col-xl-4">
          <div class="card">
            <div class="card-body">
              <h4 class="card-title mb-4">Customer Reviews</h4>
              <div class="text-center mb-4">
                <div class="font-size-36 text-primary font-weight-bold mb-1">4.8</div>
                <div class="text-muted">Average Rating</div>
              </div>
              <div class="text-center mb-5">
                <i class="mdi mdi-star text-warning"></i>
                <i class="mdi mdi-star text-warning"></i>
                <i class="mdi mdi-star text-warning"></i>
                <i class="mdi mdi-star text-warning"></i>
                <i class="mdi mdi-star-half text-warning"></i>
              </div>
              <div v-for="review in reviews" :key="review.id" class="mb-4 pb-4 border-bottom">
                <div class="d-flex align-items-center mb-2">
                  <img :src="review.image" alt class="avatar-xs rounded-circle mr-2" />
                  <div>
                    <div class="font-weight-medium">{{ review.name }}</div>
                    <div class="text-muted text-sm">{{ review.date }}</div>
                  </div>
                </div>
                <p class="text-muted">{{ review.comment }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Latest Transaction -->
        <div class="col-xl-4">
          <div class="card">
            <div class="card-body">
              <h4 class="card-title mb-4">Latest Transaction</h4>
              <WidgetTransaction :transactions="transactions" />
            </div>
          </div>
        </div>
      </div>
      <!-- end row -->

      <!-- Chat Component -->
      <div class="row">
        <div class="col-xl-4">
          <div class="card">
            <WidgetChat :chatMessages="chatMessages" />
          </div>
        </div>
      </div>
      <!-- end row -->
    </div> <!-- container-fluid -->
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import WidgetStat from '../components/widgets/widget-stat.vue';
import WidgetChart from '../components/widgets/chart.vue';
import WidgetActivity from '../components/widgets/activity.vue';
import WidgetTransaction from '../components/widgets/transaction.vue';
import WidgetChat from '../components/widgets/chat.vue';

export default {
  name: 'DashboardPage',
  components: {
    WidgetStat,
    WidgetChart,
    WidgetActivity,
    WidgetTransaction,
    WidgetChat
  },
  setup() {
    // Mock data for activity feed
    const activityData = ref([
      { id: 1, date: 'Today 09:45', text: 'New user registered' },
      { id: 2, date: 'Today 08:30', text: 'Product added to cart' },
      { id: 3, date: 'Yesterday 18:20', text: 'Payment received' },
      { id: 4, date: 'Yesterday 15:10', text: 'Order shipped' },
      { id: 5, date: '2 days ago', text: 'New product added' }
    ]);

    // Mock data for transactions
    const transactions = ref([
      { id: 1, name: 'John Doe', date: 'Today 10:30', amount: '$250', status: 'Delivered', image: '@/assets/images/users/user-1.jpg' },
      { id: 2, name: 'Jane Smith', date: 'Today 09:15', amount: '$120', status: 'Pending', image: '@/assets/images/users/user-2.jpg' },
      { id: 3, name: 'Mike Johnson', date: 'Yesterday 18:45', amount: '$350', status: 'Delivered', image: '@/assets/images/users/user-3.jpg' },
      { id: 4, name: 'Sarah Wilson', date: 'Yesterday 14:20', amount: '$85', status: 'Cancel', image: '@/assets/images/users/user-4.jpg' },
      { id: 5, name: 'Robert Brown', date: '2 days ago', amount: '$190', status: 'Delivered', image: '@/assets/images/users/user-5.jpg' }
    ]);

    // Mock data for chat messages
    const chatMessages = ref([
      { id: 1, name: 'John', message: 'Hello, how can I help you?', time: '10:30', odd: false, image: '@/assets/images/users/user-1.jpg' },
      { id: 2, name: 'Customer', message: 'I have a question about your product.', time: '10:32', odd: true, image: '@/assets/images/users/user-2.jpg' },
      { id: 3, name: 'John', message: 'Sure, please feel free to ask.', time: '10:33', odd: false, image: '@/assets/images/users/user-1.jpg' },
      { id: 4, name: 'Customer', message: 'How long is the delivery time?', time: '10:35', odd: true, image: '@/assets/images/users/user-2.jpg' },
      { id: 5, name: 'John', message: 'It usually takes 2-3 business days.', time: '10:36', odd: false, image: '@/assets/images/users/user-1.jpg' }
    ]);

    // Mock data for popular products
    const popularProducts = ref([
      { id: 1, name: 'Product A', sales: '1,250', image: '@/assets/images/small/img-1.jpg' },
      { id: 2, name: 'Product B', sales: '950', image: '@/assets/images/small/img-2.jpg' },
      { id: 3, name: 'Product C', sales: '820', image: '@/assets/images/small/img-3.jpg' },
      { id: 4, name: 'Product D', sales: '680', image: '@/assets/images/small/img-4.jpg' }
    ]);

    // Mock data for reviews
    const reviews = ref([
      { id: 1, name: 'John Doe', date: '2 days ago', comment: 'Great product and fast delivery!', image: '@/assets/images/users/user-1.jpg' },
      { id: 2, name: 'Jane Smith', date: '1 week ago', comment: 'Very satisfied with my purchase.', image: '@/assets/images/users/user-2.jpg' }
    ]);

    // Initialize chart when component mounts
    onMounted(() => {
      // You can add chart initialization code here if needed
      // For now, we're using the basic chart component
    });

    return {
      activityData,
      transactions,
      chatMessages,
      popularProducts,
      reviews
    };
  },
};
</script>

<style scoped>
/* 从npm包导入bootstrap 5.0.1 */
@import 'bootstrap/dist/css/bootstrap.min.css';
@import '@/assets/css/icons.min.css';
@import '@/assets/css/app.min.css';
</style>